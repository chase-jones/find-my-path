from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

import numpy as np
import pandas as pd

# initialize food data
df_test = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/New Full SKU List.csv')

# input grocerylist
myGroceryList = ['AGAVE,DRIED (SOUTHWEST)','ACORNS,DRIED','ALLSPICE,GROUND','ALMONDS,BLANCHED']

def df_itemtoid(aList,df):
    id_list = []
    for item in aList:
        id_list.append(df.loc[df['Description'] == item ,'Id'].values[0])
    res=pd.DataFrame(id_list,columns=['Id'])
    return res

def df_idtozone(aList,df): # modified to include entrance and exit in zone list
    zone_list = [-1]
    for item in aList:
        zone_list.append(df.loc[df['Description'] == item, 'Zone Number'].values[0])
    zone_list.append(999999999)
    result=pd.DataFrame(zone_list,columns =['Zone'])
    return result

def df_idzone(df1,df2):
#merge both data frames
    frames=[df1,df2]
    df_f = pd.concat(frames,axis=1)
    return df_f

t1=df_itemtoid(myGroceryList,df_test)
t2=df_idtozone(myGroceryList,df_test)
sol=df_idzone(t1,t2)

#  sofia code - reduce matrix
data = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/Zone Distanced Pivoted.csv', index_col=0)

# alternative code if we would prefer to append the entrance/exit outside of nicole's function
# method 1: t2 = t2.append({'Zone': 999999999}, ignore_index=True) # adds checkout 'zone' to the end of the matrix
# method 2: t2.loc[len(t2)] = 999999999
# # lines 1, 2, 3 below add entrance 'zone' to the beginning of the matrix
# t2.loc[-1] = [-1] # [1]
# t2.index = t2.index + 1 # [2]
# t2 = t2.sort_index() # [3]

# print('after appending enter/exit',t2)

def reduce_loc(zones_dataframe):
    zone_list = zones_dataframe['Zone'].tolist()
    colnames = []
    for x in zone_list:
        colnames.append(str(x))
    return data.loc[zone_list,colnames].head()

solver_distmx = reduce_loc(t2)
print(solver_distmx)

### TSP SOLVER ###
# this version uses the sample CSV_Nicole
s_distmx = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/CSV_Nicole.csv', index_col=0, encoding='latin-1', engine='python')
solver_distmx = s_distmx.values.tolist()

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = solver_distmx # to solve the problem we use the solver_distmx in list form
    data['num_vehicles'] = 1
    data['starts'] = [0]
    data['ends'] = [len(solver_distmx)-1]
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    index = routing.Start(0)
    plan_output = 'Building route for customer list...\n'
    route_distance = 0
    listoutput = [] # used to build list output
    while not routing.IsEnd(index):
        listoutput.append(s_distmx.columns[index]) # appends zone number to list. to build the headers we use the pandas dataframe
        if index == 0:
            plan_output += '\n Start at store entrance.' # store entrance will always be first
        else:
            plan_output += '\n Go to Zone %s ' %(s_distmx.columns[index]) # used to build 'user friendly' output
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, 0)
    plan_output += '\n Go to checkout.' # checkout will always be last
    listoutput.append(s_distmx.columns[index])
    for i in range(len(listoutput)):
        listoutput[i] = int(listoutput[i])
    plan_output += '\n Distance of the route: {}m\n'.format(route_distance)
    print(plan_output)
    print(listoutput)

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
