import pandas as pd
import numpy as np


def init(bigdf):
    pass


def main():
    df_grocery_list = pd.read_csv('100 Random Rows.csv')
    df_big_matrix = pd.read_csv('Distance Data Pivot.csv')
    df_item_descriptions = df_grocery_list.loc[:, "Description"]


if __name__ == '__main__':
    main()


def df_item_desc_to_id(item_list, df_all_skus):  # used to build sol dataframe
    id_list = []
    for item in item_list:
        id_list.append(df_all_skus.loc[df_all_skus['Description'] == item, 'Id'].values[0])
    res = pd.DataFrame(id_list, columns=['Id'])
    return res


def df_id_to_item_desc(desc_list, df_all_skus):
    dsc_list = []
    for item in desc_list:
        dsc_list.append(df_all_skus.loc[df_all_skus['Id'] == item, 'Description'].values[0])
    res = pd.DataFrame(dsc_list, columns=['Description'])
    return res


def df_id_to_zone(df_id, df_all_skus):
    zone_list = []
    id_list = df_id['Id'].tolist()
    for item in id_list:
        zone_list.append(df_all_skus.loc[df_all_skus['Id'] == item, 'Zone'].values[0])
    result = pd.DataFrame(zone_list, columns=['Zone'])
    return result


# def df_concat_id_and_zone(df_id, df_zone):
# #merge both data frames
#     frames=[df_id, df_zone]
#     df_f = pd.concat(frames,axis=1)
#     return df_f


def df_id_to_zone_with_enter_exit(df_id, df_all_skus):  # used to build the matrix needed for the OR solver
    zone_list = [-1]
    id_list = df_id['Id'].tolist()
    for item in id_list:
        zone_list.append(df_all_skus.loc[df_all_skus['Id'] == item, 'Zone Number'].values[0])
    zone_list.append(999999999)
    result = pd.DataFrame(zone_list, columns=['Zone'])
    return result


def df_id_zone_combine(list_user_input_groceries, df_id,
                       df_zone):  # builds sol dataframe with description, id, and zone
    # merge both data frames
    desc = pd.DataFrame(list_user_input_groceries, columns=['Description'])
    frames = [desc, df_id, df_zone]
    df_f = pd.concat(frames, axis=1)
    return df_f


def df_get_full_reduced_list_by_id(df_id, df_all_skus):
    list_id = df_id.values.tolist()[0]
    return df_all_skus[df_all_skus['Id'].isin(list_id)]


def df_replace_zeros_with_nines(df):
    df = df.replace(to_replace=0, value=99999)
    return df


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


def reduce_loc(df_zones, df_large_pivot):
    zone_list = df_zones['Zone'].tolist()
    colnames = []
    for x in zone_list:
        colnames.append(str(x))
    df1 = df_large_pivot[colnames]
    df2 = df1[df1.index.isin(zone_list)]
    return df2


def get_single_desc(df_ids_and_zones,
                    int_zone_number):  # takes in a zone, returns a list of items needed from that zone
    temp_series = df_ids_and_zones.loc[df_ids_and_zones['Zone'] == int_zone_number, 'Description']  # .item()
    result = []
    for index, int_zone_number in temp_series.items():
        result.append(int_zone_number)
    return result
