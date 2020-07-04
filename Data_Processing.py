import pandas as pd
import numpy as np


def main():
    df_grocery_list = pd.read_csv('100 Random Rows.csv')
    df_big_matrix = pd.read_csv('Distance Data Pivot.csv')
    df_item_descriptions = df_grocery_list.loc[:, "Description"]


if __name__ == '__main__':
    main()

def reduce_loc(zones_dataframe):
    zone_list = zones_dataframe['Id'].tolist()
    colnames = []
    for x in zone_list:
        colnames.append(str(x))
    return data.loc[zone_list,colnames].head()

def df_item_to_id(aList, df):
    id_list = []
    for item in aList:
        id_list.append(df.loc[df['Description'] == item, 'Id'].values[0])
    res = pd.DataFrame(id_list, columns=['Id'])
    return res


def df_id_to_zone(aList, df):
    zone_list = []
    for item in aList:
        zone_list.append(df.loc[df['Description'] == item, 'Zone'].values[0])
    result = pd.DataFrame(zone_list, columns=['Zone'])
    return result


def df_id_zone_combine(df1, df2):
    # merge both data frames
    frames = [df1, df2]
    df_f = pd.concat(frames, axis=1)
    return df_f


def get_ordered_id_list(df_list_ids_and_zones, df_ordered_zones):
    output_df = pd.DataFrame(columns=['Order_num', 'Item_ID'])
    i = 1
    for index, value in df_ordered_zones.items():
        # Generates a series based on the current zone. Stores in temp_series
        temp_series = df_list_ids_and_zones.loc[df_list_ids_and_zones['Zone'] == value, 'Id']

        for index, value in temp_series.items():
            new_row = {'Order_num': i, 'Item_ID': value}
            output_df = output_df.append(new_row, ignore_index=True)
            i += 1
    return output_df

