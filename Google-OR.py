from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

import numpy as np
import pandas as pd

# nicole code - read from csv
df_test = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/New Full SKU List.csv')

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

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = solver_distmx # example had it as list but pandas df seems to work
    # yapf: disable
    data['num_vehicles'] = 1
    data['starts'] = [0] # first item, index of start location, needs to be array
    data['ends'] = [len(solver_distmx)] #last item, index of end location, needs to be array
    return data

data = create_data_model()
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                       data['num_vehicles'], data['starts'], data['ends'])
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)

routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

def print_solution(data, manager, routing, solution):
    print('Objective: {} feet'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for customer:\n'
    route_distance = 0
    output = []
    while not routing.IsEnd(index):
        output.append(solver_distmx.columns[index]) # appends zone number
        plan_output += '\n From Zone {}, get %s -> '.format(manager.IndexToNode(index)) # this will map the indices, not zones.. printing to show that the solver works
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += '\n Go to checkout.' # in the original code it sent us back to 0 here.
    #plan_output += 'Zone {}\n'.format(manager.IndexToNode(index)) #editing this only affected the very last Zone 0 (last point) so the last point must not be attached to the rest of the code
    print(plan_output)
    plan_output += 'Route distance: {}feet\n'.format(route_distance)
    print('List form output:', output)

solution = routing.SolveWithParameters(search_parameters)
if solution:
    print_solution(manager, routing, solution)

# # chase's code
#     def main():
#         df_grocery_list = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/100 Random Rows.csv')
#         df_big_matrix = pd.read_csv('C:/Users/satzr/Desktop/Senior Design/GoogleTSPwithClasses/Distance Data Pivot.csv')
#         df_item_descriptions = df_grocery_list.loc[:, "Description"]
#
#     if __name__ == '__main__':
#         main()
#
#     def get_ordered_id_list(df_list_ids_and_zones, df_ordered_zones):
#         output_df = pd.DataFrame(columns=['Order_num', 'Item_ID'])
#         i = 1
#         for index, value in df_ordered_zones.items():
#             # Generates a series based on the current zone. Stores in temp_series
#             temp_series = df_list_ids_and_zones.loc[df_list_ids_and_zones['Zone'] == value, 'Id']
#
#             for index, value in temp_series.items():
#                 new_row = {'Order_num': i, 'Item_ID': value}
#                 output_df = output_df.append(new_row, ignore_index=True)
#                 i += 1
#         return output_df
#
#     def id_desc(id, df):
#         return df.loc[df['Id' == id, 'Description'].values[0]]