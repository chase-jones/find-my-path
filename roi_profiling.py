from __future__ import print_function
import pandas as pd
#import CplexOR as cor
import GoogleOR as gor
import Data_Processing as dp

import psutil
import os

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def mainGG():
    df_zone_pivot = pd.read_csv('New Zone Distanced Pivoted Integers Only.csv', index_col=0)
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

    df_roi = pd.DataFrame(columns=['filename', 'cpu', 'memory', '# threads','# handles','cpuseconds'])
    for cart in array_cart_dictionaries:
        mainGOR(cart)
        current_frequency = str(psutil.cpu_freq()[0]/1000) + 'GHz'

        pid = os.getpid()
        py = psutil.Process(pid)
        with py.oneshot():
            n_threads = py.num_threads()
            n_handles = py.num_handles()
            uss = get_size(py.memory_full_info()[-1])
            system_cputime_seconds = py.threads()[0][2] # system cpu time for thread

        df_roi = df_roi.append(
            {'filename': cart.get("File Name"), 'cpu': current_frequency,'memory': uss,'# threads': n_threads,'# handles':n_handles,'cpuseconds':system_cputime_seconds}, ignore_index=True)

        df_roi.to_csv('GoogleROIValues.csv', index=False)

def mainGOR(cart):
    cart.update({'Solved OR Zones': gor.solve_tsp(cart.get("Reduced df"))[0]})
    list1 = cart.get('Solved OR Zones')
    list1.pop(len(list1) - 1)
    list1.pop(0)
    series1 = pd.Series(list1, name='Id')
    cart.update({'Ordered Item list by id': dp.get_ordered_id_list(cart.get('Reduced SKU List'), series1)})

def mainCP():
    df_zone_pivot = pd.read_csv('New Zone Distanced Pivoted Integers Only.csv', index_col=0)
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

    df_roi = pd.DataFrame(columns=['filename', 'cpu', 'memory', '# threads', '# handles', 'cpuseconds'])
    for cart in array_cart_dictionaries:
        mainCOR(cart)
        current_frequency = str(psutil.cpu_freq()[0] / 1000) + 'GHz'

        pid = os.getpid()
        py = psutil.Process(pid)
        with py.oneshot():
            n_threads = py.num_threads()
            n_handles = py.num_handles()
            uss = get_size(py.memory_full_info()[-1])
            system_cputime_seconds = py.threads()[0][2]  # system cpu time for thread

        df_roi = df_roi.append(
            {'filename': cart.get("File Name"), 'cpu': current_frequency, 'memory': uss, '# threads': n_threads,
             '# handles': n_handles, 'cpuseconds': system_cputime_seconds}, ignore_index=True)

        df_roi.to_csv('CplexROIValues.csv', index=False)

def mainCOR(cart):
    cart.update({'Solved OR Zones': cor.solution(cart.get("Reduced df 2"))[0]})

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

