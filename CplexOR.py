import numpy as np
import pandas as pd
import time
import pyomo.environ as pyEnv

#Make sure to run this before running the whole code!!!!!!!!

#export PATH=/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:$PATH


def main():
    cost_matrix=pd.read_csv('/Users/nicolenarvaez/Downloads/CSV_Nicole.csv')
    print(cost_matrix)
    solution(cost_matrix)

def solution(cost_matrix):
    n = len(cost_matrix)
    zone_list = cost_matrix.columns
    c_matrix=cost_matrix.to_numpy()
#Model
    model = pyEnv.ConcreteModel()

#Indexes for the cities
    model.M = pyEnv.RangeSet(n)
    model.N = pyEnv.RangeSet(n)

#Index for the dummy variable u
    model.U = pyEnv.RangeSet(2,n)

#Decision variables xij
    model.x=pyEnv.Var(model.N,model.M, within=pyEnv.Binary)

#Dummy variable ui
    model.u=pyEnv.Var(model.N, within=pyEnv.NonNegativeIntegers,bounds=(0,n-1))

#Cost Matrix cij
    model.c = pyEnv.Param(model.N, model.M,initialize=lambda model, i, j: c_matrix[i-1][j-1])



    def obj_func(model):
        return sum(model.x[i,j] * model.c[i,j] for i in model.N for j in model.M)

    model.objective = pyEnv.Objective(rule=obj_func,sense=pyEnv.minimize)

#Constraint 1
    def rule_const1(model,M):
        return sum(model.x[i,M] for i in model.N if i!=M ) == 1

    model.const1 = pyEnv.Constraint(model.M,rule=rule_const1)

#Constraint 2
    def rule_const2(model,N):
        return sum(model.x[N,j] for j in model.M if j!=N) == 1

    model.rest2 = pyEnv.Constraint(model.N,rule=rule_const2)

# Constraint 3
    def rule_const3(model, i, j):
        if i != j:
            return model.u[i] - model.u[j] + model.x[i, j] * n <= n - 1
        else:
            # Yeah, this else doesn't say anything
            return model.u[i] - model.u[i] == 0


    model.rest3 = pyEnv.Constraint(model.U, model.N, rule=rule_const3)




    #Constraint 4 -- constraint that will be able to assure that (999,1)==1
    def rule_const4(model):
        return model.x[1,n] == 0

    model.rest4 = pyEnv.Constraint(rule=rule_const4)

    def rule_const5(model):
        return model.x[n,1] == 1

    model.rest5 = pyEnv.Constraint(rule=rule_const5)


#Prints the entire model
    #model.pprint()


    solver=pyEnv.SolverFactory('cplex')
    result=solver.solve(model, tee=False)
    #print(type(result))


#PRINTS DECISION VARIABLES

    List = list(model.x.keys())

#breakpoint -- can check memory (list might already exist)

    #for i in List:
        #if model.x[i]() != 0:
            #print(i,'--',model.x[i]())

##DESIRED OUTPUT

    path = []
    #space
    for j in List:
        if model.x[j]() !=0:
            path.append(j)


#function starts with 1 to give path
    def get_path(start, path1):
        aPath=[]
        aX=[]
        aY=[]
        for r in path1:
            aX.append(r[0])
            aY.append(r[1])
        aPath.append(start)
        for i in range(n-1):
            aPath.append(aY[aPath[i]-1])
        return aPath


    test=get_path(1,path)



    ordered_zones=[]
    for k in test:
        if k == len(zone_list):
            ordered_zones.append(zone_list[k-1])
        else:
            ordered_zones.append(zone_list[k-1])


    ordered_zones_pd=pd.Series(ordered_zones)
    print(model.objective())
    return ordered_zones_pd




if __name__ == "__main__":
    main()


