import pandas as pd
import numpy as np
# import Image_Processing as ip
# import CplexOR as cor
import GoogleOR as gor
import Data_Processing as dp
import os

def testgor(): # sofia used this function to make sure google or was working correctly - it can be deleted if it is no longer necessary
    df_zone_pivot = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    df_full_sku_list = pd.read_csv('New Full SKU List.csv')
    myGroceryList = ['AGAVE,DRIED (SOUTHWEST)', 'ACORNS,DRIED', 'ALLSPICE,GROUND', 'ALMONDS,BLANCHED']

    ids = dp.df_item_desc_to_id(myGroceryList, df_full_sku_list)
    df = dp.df_id_to_zone_with_enter_exit(ids, df_full_sku_list)
    print(df)
    single_cart = {
        "Reduced df": dp.reduce_loc(df, df_zone_pivot),
        "Id df": myGroceryList,
        "Reduced SKU List": dp.df_get_full_reduced_list_by_id(ids, df_full_sku_list),
        "Reduced df 2": dp.df_replace_zeros_with_nines(dp.reduce_loc(df, df_zone_pivot))
    }

    return print(gor.solve_tsp(dp.reduce_loc(df,df_zone_pivot)))
# testgor()

def main():
    df_zone_pivot = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    df_full_sku_list = pd.read_csv('New Full SKU List.csv')
    array_all_shopping_carts = load_shopping_cart_list("Shopping Carts")

    array_cart_dictionaries = []

    for id_df in array_all_shopping_carts:
        df = dp.df_id_to_zone_with_enter_exit(id_df, df_full_sku_list)
        single_cart = {
            "Reduced df": dp.reduce_loc(df, df_zone_pivot),
            "Id df": id_df,
            "Reduced SKU List": dp.df_get_full_reduced_list_by_id(id_df, df_full_sku_list),
            "Reduced df 2": dp.df_replace_zeros_with_nines(dp.reduce_loc(df, df_zone_pivot))
        }
        array_cart_dictionaries.append(single_cart)

    # # add this code back when you start to run carts full of descriptions, not ids
    # for reduced_distance_matrix, df_id_zone_desc in zip(array_all_reduced_dfs,array_all_df_id_zone_description):
    #     gor.solve_tsp(reduced_distance_matrix, df_id_zone_desc)

    for cart in array_cart_dictionaries:
        cart.update({'Solved OR Zones': gor.solve_tsp(cart.get("Reduced df 2"))})
        # Maintaining list variable so we can remove the first and last zones from the list
        list1 = cart.get('Solved OR Zones')
        list1.pop(len(list1) - 1)
        list1.pop(0)
        series1 = pd.Series(list1, name='Id')
        cart.update({'Ordered Item list by id': dp.get_ordered_id_list(cart.get('Reduced SKU List'), series1)})
        print(cart)
    print('test')

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
    main()
