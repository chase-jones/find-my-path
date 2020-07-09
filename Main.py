import A_Star_Routing_2 as astar
import pandas as pd
import numpy as np
import Image_Processing as ip


def main():
    image_df = ip.read_image("Test Maze.png")
    all_combos = all_pixel_combos(image_df)
    all_combos_2 = all_combos.drop_duplicates()

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
            new_row = {'X': row, 'Y': col}
            already_checked = already_checked.append(new_row, ignore_index=True)

            for col1 in image_df.columns:
                for row2 in image_df.index:
                    pass #placeholder


    return combination_df


if __name__ == "__main__":
    main()
