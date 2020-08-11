"""
Main file

Takes in full pivoted file which contains distances between all of the zones
Takes in full SKU list [Inlcludes item IDs and zones]


"""

import pandas as pd
import GoogleOR as gor
import Data_Processing as dp
import os


def main():
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
        solve_and_update_cart(cart)
        

def solve_and_update_cart(cart):
    cart.update({'Solved OR Zones': gor.solve_tsp(cart.get("Reduced df"))[0]})
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
    main()
