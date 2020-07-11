import pandas as pd
import numpy as np
# import Image_Processing as ip
# import CplexOR as cor
import os


def main():
    all_shopping_carts_array = load_shopping_cart_list("Shopping Carts")
    print(len(all_shopping_carts_array))

def load_shopping_cart_list(shopping_cart_folder):
    a1 = []
    for filename in os.listdir(shopping_cart_folder):
        if filename.endswith(".csv"):
            a1.append(load_shopping_cart((shopping_cart_folder + '/' + filename)))
    return a1


def load_shopping_cart(shopping_cart_path):
    df = pd.read_csv(shopping_cart_path, ignore_index = True, columns = ['Items'])
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
