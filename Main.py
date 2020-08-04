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

def group_by_items(array_cart_orderedids):
    group, members = [], set()

    for item in array_cart_orderedids:
        if group and members.isdisjoint(item):
            yield group
            group, members = [], set()
        group.append(item)
        members.update(item)

    yield group

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

    for cart in array_cart_dictionaries:
        for i in range(10):
            csvname = 'googl_' + cart.get("File Name") + '_' + str(i) + '.csv' # change this name to reflect the cart size we are testing
            pr = cProfile.Profile()
            pr.enable()
            mainGOR(cart)
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

def mainGOR(cart):
    cart.update({'Solved OR Zones': gor.solve_tsp(cart.get("Reduced df"))})
    # Maintaining list variable so we can remove the first and last zones from the list
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


def main2():
    image_df = pd.read_csv('Image_df.csv', index_col=0)

    all_combos = all_pixel_combos(image_df)
    all_combos.describe()
    all_combos_2 = all_combos.drop_duplicates()
    all_combos_2.describe()
    pass
    # df_zone = pd.read_csv('ZoneList.csv')
    # df_all = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    # reduced_df = dp.reduce_loc(df_zone,df_all)
    # print(reduced_df)


def all_pixel_combos(image_df):
    combination_df = pd.DataFrame(columns=['X1', 'Y1', 'X2', 'Y2'])
    already_checked = pd.DataFrame(columns=['X', 'Y'])

    # Sort by
    for col in image_df.columns:
        for row in image_df.index:
            for col2 in image_df.columns:
                for row2 in image_df.index:
                    if image_df.loc[row, col] != 0 and image_df.loc[row2, col2] != 0:
                        new_row = {'X1': row, 'Y1': col, 'X2': row2, 'Y2': col2}
                        combination_df = combination_df.append(new_row, ignore_index=True)

    return combination_df

if __name__ == "__main__":
    mainGG()
    # run mainGG to profile the google OR solver
    # run mainCP to profile the cplex OR solver
    # to change which shopping carts are being run, you need to change the "Shopping Carts" folder in two places in each solver.
