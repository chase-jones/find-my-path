import pandas as pd
import numpy as np
# import Image_Processing as ip
#import CplexOR as cor
import GoogleOR as gor
import Data_Processing as dp
import os

import cProfile
import pstats
import io

def mainGG():
    df_zone_pivot = pd.read_csv('New Zone Distanced Pivoted Integers Only.csv', index_col=0)
    df_full_sku_list = pd.read_csv('New Full SKU List.csv')
    array_cart_dictionaries = []

    for filename in os.listdir("Shopping Carts 3"):
        if filename.endswith(".csv"):
            id_df = pd.read_csv('Shopping Carts 3' + '/' + filename, header=None)
            id_df.columns=['Id']
            df = dp.df_id_to_zone_with_enter_exit(id_df, df_full_sku_list)
            filename = filename[:-4]
            single_cart = {
                "Reduced df": dp.reduce_loc(df, df_zone_pivot),
                "Id df": id_df,
                "Reduced SKU List": dp.df_get_full_reduced_list_by_id(id_df, df_full_sku_list),
                "Reduced df 2": dp.df_replace_zeros_with_nines(dp.reduce_loc(df, df_zone_pivot)),
                "File Name": filename
            }
            array_cart_dictionaries.append(single_cart)

    df_objective = pd.DataFrame(columns = ['solver', 'cart size', 'cart sample', 'run number', 'objective function','ordered zones'])
    for cart in array_cart_dictionaries:
        firsthalf = cart.get("File Name").split('S')
        ssize = firsthalf[1][2:]
        sampnum =firsthalf[2][2:]
        for i in range(10):
            mainGOR(cart)
            df_objective = df_objective.append({'solver': 'google', 'cart size': ssize, 'cart sample': sampnum, 'run number': i, 'objective function': cart.get("Objective Function"),'ordered zones': cart.get('Solved OR Zones')}, ignore_index=True)

    df_objective.to_csv('GoogleObjectiveValues.csv',index=False)

def mainGOR(cart):
    result = gor.solve_tsp(cart.get("Reduced df"))
    cart.update({'Solved OR Zones': result[0]})
    cart.update({'Objective Function': result[1]})

def mainCP():
    df_zone_pivot = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    df_full_sku_list = pd.read_csv('New Full SKU List.csv')
    array_cart_dictionaries = []

    for filename in os.listdir("Shopping Carts 3"):
        if filename.endswith(".csv"):
            id_df = pd.read_csv('Shopping Carts 3' + '/' + filename, header=None)
            id_df.columns = ['Id']
            df = dp.df_id_to_zone_with_enter_exit(id_df, df_full_sku_list)
            filename = filename[:-4]
            single_cart = {
                "Reduced df": dp.reduce_loc(df, df_zone_pivot),
                "Id df": id_df,
                "Reduced SKU List": dp.df_get_full_reduced_list_by_id(id_df, df_full_sku_list),
                "Reduced df 2": dp.df_replace_zeros_with_nines(dp.reduce_loc(df, df_zone_pivot)),
                "File Name": filename
            }
            array_cart_dictionaries.append(single_cart)

    for cart in array_cart_dictionaries:
        for i in range(10):
            csvname = 'cplex_' + cart.get("File Name") + '_' + str(i) + '.csv'
            pr = cProfile.Profile()
            pr.enable()
            mainCOR(cart)
            pr.disable()

            result = io.StringIO()
            pstats.Stats(pr, stream=result).sort_stats('cumulative').print_stats()
            result = result.getvalue()
            # chop the string into a csv-like buffer
            result = 'ncalls' + result.split('ncalls')[-1]
            result = '\n'.join([','.join(line.rstrip().split(None, 5)) for line in result.split('\n')])
            # save it to disk

            with open(csvname, 'w+') as f:
                # f=open(result.rsplit('.')[0]+'.csv','w')
                f.write(result)
                f.close()

def mainCOR(cart):
    cart.update({'Solved OR Zones': cor.solution(cart.get("Reduced df 2"))})
    # Maintaining list variable so we can remove the first and last zones from the list
    list1 = cart.get('Solved OR Zones')
    list1.pop(len(list1) - 1)
    list1.pop(0)
    series1 = pd.Series(list1, name='Id')
    cart.update({'Ordered Item list by id': dp.get_ordered_id_list(cart.get('Reduced SKU List'), series1)})

def load_shopping_cart_list(shopping_cart_folder):
    a1 = []
    for filename in os.listdir(shopping_cart_folder):
        if filename.endswith(".csv"):
            a1.append(load_shopping_cart((shopping_cart_folder + '/' + filename)))
    return a1


def load_shopping_cart(shopping_cart_path):
    df = pd.read_csv(shopping_cart_path, header=None)
    df.columns = ['Id']
    return df

if __name__ == "__main__":
    mainGG()
    # run mainGG to profile the google OR solver
    # run mainCP to profile the cplex OR solver
    # to change which shopping carts are being run, you need to change the "Shopping Carts" folder in two places in each solver.
