from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
import pandas as pd

# initialize food data
df_test = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/New Full SKU List.csv')

# input grocerylist
myGroceryList = ['AGAVE,DRIED (SOUTHWEST)','ACORNS,DRIED','ALLSPICE,GROUND','ALMONDS,BLANCHED']

def df_itemtoid(aList,df): #used to build sol dataframe
    id_list = []
    for item in aList:
        id_list.append(df.loc[df['Description'] == item ,'Id'].values[0])
    res=pd.DataFrame(id_list,columns=['Id'])
    return res

def df_idtozone(aList,df): # used to build sol dataframe
    zone_list = []
    for item in aList:
        zone_list.append(df.loc[df['Description'] == item, 'Zone Number'].values[0])
    result=pd.DataFrame(zone_list,columns =['Zone'])
    return result

def df_idtozone_withenterexit(aList,df): # modified to include entrance and exit in zone list
    zone_list = [-1]
    for item in aList:
        zone_list.append(df.loc[df['Description'] == item, 'Zone Number'].values[0])
    zone_list.append(999999999)
    result=pd.DataFrame(zone_list,columns =['Zone'])
    return result

def df_idzone(df1,df2): # builds sol dataframe with description, id, and zone
    # merge both data frames
    desc = pd.DataFrame(myGroceryList,columns=['Description'])
    frames=[desc,df1,df2]
    df_f = pd.concat(frames,axis=1)
    return df_f

def reduce_loc(zones_dataframe, data):
    zone_list = zones_dataframe['Zone'].tolist()
    colnames = []
    for x in zone_list:
        colnames.append(str(x))
    df1 = data[colnames]
    df2 = df1[df1.index.isin(zone_list)]
    return df2

def get_ordered_id_list(df_list_ids_and_zones, list_ordered_zones): # creates dataframe with the order to pick up items by item id
    output_df = pd.DataFrame(columns=['Order_num', 'Item_ID'])
    i = 1
    for value in list_ordered_zones:
        # Generates a series based on the current zone. Stores in temp_series
        temp_series = df_list_ids_and_zones.loc[df_list_ids_and_zones['Zone'] == value, 'Id']

        for index, value in temp_series.items():
            new_row = {'Order_num': i, 'Item_ID': value}
            output_df = output_df.append(new_row, ignore_index=True)
            i += 1
    return output_df

def get_singledesc(df_list_ids_and_zones, value): # takes in a zone, returns the items needed from that zone
    temp_series = df_list_ids_and_zones.loc[df_list_ids_and_zones['Zone'] == value, 'Description'] #.item()
    result = []
    for index, value in temp_series.items():
        result.append(value)
    return result

t1=df_itemtoid(myGroceryList,df_test)
t2=df_idtozone(myGroceryList,df_test)
t3=df_idtozone_withenterexit(myGroceryList,df_test)
sol=df_idzone(t1,t2)

#  initialize zone pivot data
data = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/Zone Distanced Pivoted.csv', index_col=0)

s_distmx = reduce_loc(t3, data)
solver_distmx = s_distmx.values.tolist()

def create_data_model():
    data = {}
    data['distance_matrix'] = solver_distmx # to solve the problem we use the solver_distmx in list form
    data['num_vehicles'] = 1
    data['starts'] = [0]
    data['ends'] = [len(solver_distmx)-1]
    return data

def print_solution(data, manager, routing, solution):
    index = routing.Start(0)
    plan_output = 'Building route for customer list...\n'
    route_distance = 0
    listoutput = [] # used to build list output for future program use
    while not routing.IsEnd(index):
        zonenumber = s_distmx.columns[index] # to build the headers we use the pandas dataframe. zonenumber is a string (column header)
        itemdescription = get_singledesc(sol,int(zonenumber))
        listoutput.append(int(zonenumber)) # appends zone number to list.
        if index == 0:
            plan_output += '\n Start at store entrance.' # store entrance will always be first
        else:
            plan_output += '\n Go to Zone %s and get %s.' %(zonenumber, itemdescription) # used to build 'user friendly' output
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, 0)
    plan_output += '\n Go to checkout.' # checkout will always be last
    listoutput.append(int(s_distmx.columns[index]))
    plan_output += '\n Distance of the route: {}m\n'.format(route_distance) # route_distance is an integer
    print(plan_output)
    print(listoutput)
    
    df_orderedids = get_ordered_id_list(sol,listoutput)
    print(df_orderedids)

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        999999,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == '__main__':
    main()
