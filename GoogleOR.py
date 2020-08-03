from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def solve_tsp(s_distmx):

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
        # plan_output = 'Building route for customer list...\n'
        route_distance = 0
        listoutput = []
        while not routing.IsEnd(index):
            zonenumber = s_distmx.columns[index] # to build the headers we use the pandas dataframe. zonenumber is a string (column header)
            # itemdescription = dp.get_single_desc(sol,int(zonenumber))
            listoutput.append(int(zonenumber)) # appends zone number to list.
            # if index == 0:
            #     plan_output += '\n Start at store entrance.' # store entrance will always be first
            # else:
            #     plan_output += '\n Go to Zone %s and get [item description].' %(zonenumber) # itemdescription, used to build 'user friendly' output
            # previous_index = index
            index = solution.Value(routing.NextVar(index))
            # route_distance += routing.GetArcCostForVehicle(
            #     previous_index, index, 0)
        # plan_output += '\n Go to checkout.' # checkout will always be last
        listoutput.append(int(s_distmx.columns[index]))
        # plan_output += '\n Distance of the route: {}m\n'.format(route_distance) # route_distance is an integer
        return listoutput

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
            return print_solution(data, manager, routing, solution)

    return(main())

if __name__ == "__main__":
    distancematrix_asarray = # read the csv here
    solve_tsp(distancematrix_asarray)