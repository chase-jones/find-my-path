import Data_Processing as dp
import pandas as pd
import numpy as np

def main():
    df_zone = pd.read_csv('ZoneList.csv')
    df_all = pd.read_csv('Zone Distanced Pivoted.csv', index_col=0)
    reduced_df = dp.reduce_loc(df_zone,df_all)
    print(reduced_df)

if __name__ == "__main__":
    main()
