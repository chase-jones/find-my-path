import A_Star_Routing_2 as astar
import pandas as pd
import numpy as np
import Image_Processing as ip


def main():
    image_df = pd.read_csv('Image_df.csv',index_col=0)

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
