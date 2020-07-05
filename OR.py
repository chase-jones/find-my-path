# Make sure to run this before running the whole code!!!!!!!!

# export PATH=/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:$PATH

### OUR WAY OF DIVIDING THE STORE INTO ZONES/NODES
# the storemodule class is a zone where items found in a similar location are grouped

import numpy as np
import time
import pyomo.environ as pyEnv


class StoreModule:
    def __init__(self, aisle, products):
        self.aisle = aisle  # we can change this to be a string so that it can be Aisle 1 or Produce Section, etc.
        self.products = products

    def add_products(self, items):
        self.products.append(items)

    def get_products(self):
        return self.products

    def filterproducts(self, grocerylist):
        for item in grocerylist:
            if item in self.products:
                return item

    def get_aisle(self):
        return self.aisle


# prepare each zone with a list of items

zone0 = StoreModule('0', ['milk', 'eggs'])
zone1 = StoreModule('1', ['toothpaste', 'onions'])
zone2 = StoreModule('2', ['butter', 'flour'])
zone3 = StoreModule('3', ['bleach', 'ice cream'])
zone4 = StoreModule('4', ['vinegar', 'cookies'])
zone5 = StoreModule('5', ['candy', 'juice'])

allzones = [zone0, zone1, zone2, zone3, zone4, zone5]  # this index will change as the matrix gets bigger and smaller

### INPUT GROCERY LIST ###
# myGroceryList = input('Please input your shopping list. Separate each item with one space. For example: milk eggs butter.').split(" ")
myGroceryList = ['milk', 'onions', 'butter', 'ice cream', 'juice']

cost_matrix = np.array([
    [9999, 2451, 713, 1018, 1631, 1374],
    [2451, 9999, 1745, 1524, 831, 1240],
    [713, 1745, 9999, 355, 920, 803],
    [1018, 1524, 355, 9999, 700, 862],
    [1631, 831, 920, 700, 9999, 663],
    [1374, 1240, 803, 862, 663, 9999]])

n = len(cost_matrix) - 1

# identify which zones you need to access and create list of booleans that we will use to filter the original matrix
filter_array = []
myzones = []

for zone in range(len(allzones)):
    for item in myGroceryList:
        if item in allzones[zone].products:
            filter_array.append(True)
            myzones.append(allzones[zone])
            break
    else:
        filter_array.append(False)

# reduce matrix using numpy
mydistancematrix = cost_matrix[filter_array][:, filter_array]
print(filter_array, mydistancematrix)
# convert numpy array to list
solver_distmx = mydistancematrix.tolist()
# pass this list to create_data_model function



# Model
model = pyEnv.ConcreteModel()

# creates an instance
instance = model.create_instance()

# Indexes for the cities
model.M = pyEnv.RangeSet(n)
model.N = pyEnv.RangeSet(n)

# Index for the dummy variable u
model.U = pyEnv.RangeSet(2, n)

# Decision variables xij
model.x = pyEnv.Var(model.N, model.M, within=pyEnv.Binary)

# Dummy variable ui
model.u = pyEnv.Var(model.N, within=pyEnv.NonNegativeIntegers, bounds=(0, n - 1))

# Cost Matrix cij
model.c = pyEnv.Param(model.N, model.M, initialize=lambda model, i, j: cost_matrix[i - 1][j - 1])


def obj_func(model):
    return sum(model.x[i, j] * model.c[i, j] for i in model.N for j in model.M)


model.objective = pyEnv.Objective(rule=obj_func, sense=pyEnv.minimize)


# Constraint 1
def rule_const1(model, M):
    return sum(model.x[i, M] for i in model.N if i != M) == 1


model.const1 = pyEnv.Constraint(model.M, rule=rule_const1)


# Constraint 2
def rule_const2(model, N):
    return sum(model.x[N, j] for j in model.M if j != N) == 1


model.rest2 = pyEnv.Constraint(model.N, rule=rule_const2)


# Constraint 3
def rule_const3(model, i, j):
    if i != j:
        return model.u[i] - model.u[j] + model.x[i, j] * n <= n - 1
    else:
        # Yeah, this else doesn't say anything
        return model.u[i] - model.u[i] == 0


model.rest3 = pyEnv.Constraint(model.U, model.N, rule=rule_const3)

# Prints the entire model
model.pprint()

solver = pyEnv.SolverFactory('cplex')
result = solver.solve(model, tee=False)
print(result)
print(type(result))

# PRINTS DECISION VARIABLES

List = list(model.x.keys())

# breakpoint -- can check memory (list might already exist)

for i in List:
    if model.x[i]() != 0:
        print(i, '--', model.x[i]())

##DESIRED OUTPUT

path = []

for j in List:
    if model.x[j]() != 0:
        path.append(j)


def convertTuple(aList):
    aString = ','.join(str(tup) for tup in aList)
    return aString


convertTuple(path)
aPath = []
aPath.append(path[0][0])
aPath.append(path[0][1])
aPath.append(path[4][0])
aPath.append(path[4][1])
aPath.append(path[3][0])

# PRINTS PATH

print(path)

print(path[0][0], ' > ', path[0][1], ' > ', path[4][0], ' > ', path[4][1], ' > ', path[3][0])
print(aPath)

# grocery list path
# 0-2-4-1-3
gList = []
for d in range(0, len(aPath)):
    g = int(aPath[d] - 1)
    gList.append(myGroceryList[g])

print(gList)

# need to create a loop that will loop through values in path list and print it out how we want it.....

# PRINTS TIME
print('Time:', time.process_time())

# PRINTS OBJECTIVE VAL
print('objective value:', model.objective())

# path
# returns all of the possibilities between nodes
# for j in List:
# if model.x[j]() != 0:
# aNode=convertTuple(j,List)
# print(aNode)
