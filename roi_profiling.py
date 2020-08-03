from __future__ import print_function
import pandas as pd
# import Image_Processing as ip
#import CplexOR as cor
import GoogleOR as gor
import Data_Processing as dp
import os

import cProfile
import pstats
import io

import psutil
import os

def mainGG():
    df_zone_pivot = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    df_full_sku_list = pd.read_csv('New Full SKU List.csv')
    array_cart_dictionaries = []

    for filename in os.listdir("Shopping Carts 3"):
        if filename.endswith(".csv"):
            if filename.startswith(('Sze30Smp')):
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

    for cart in array_cart_dictionaries:
        print(cart.get("File Name"))
        print('solver: google')
        mainGOR(cart)

        print('cpu % used:', psutil.cpu_percent())
        print('virtual memory', psutil.virtual_memory()) # physical memory usage
        print('memory % used:', psutil.virtual_memory()[2])

        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
        print('memory use (GB?):', memoryUse)

def mainGOR(cart):
    cart.update({'Solved OR Zones': gor.solve_tsp(cart.get("Reduced df"))})

    list1 = cart.get('Solved OR Zones')
    list1.pop(len(list1) - 1)
    list1.pop(0)
    series1 = pd.Series(list1, name='Id')
    cart.update({'Ordered Item list by id': dp.get_ordered_id_list(cart.get('Reduced SKU List'), series1)})

def mainCP():
    df_zone_pivot = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    df_full_sku_list = pd.read_csv('New Full SKU List.csv')
    array_cart_dictionaries = []

    for filename in os.listdir("Shopping Carts 3"):
        if filename.endswith(".csv"):
            if filename.startswith(('Sze30Smp1')):
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

    for cart in array_cart_dictionaries:
        print(cart.get("File Name"))
        print('solver: cplex')
        mainCOR(cart)

        print('cpu % used:', psutil.cpu_percent())
        print('virtual memory', psutil.virtual_memory()) # physical memory usage
        print('memory % used:', psutil.virtual_memory()[2])

        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
        print('memory use (GB?):', memoryUse)

def mainCOR(cart):
    cart.update({'Solved OR Zones': cor.solution(cart.get("Reduced df 2"))})

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
    #mainCP
    # run mainGG to profile the google OR solver
    # run mainCP to profile the cplex OR solver

