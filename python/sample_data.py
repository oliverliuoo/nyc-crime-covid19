import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("../data/full_data.csv")
    keep_cols = ['CMPLNT_NUM', 'ADDR_PCT_CD', 'BORO_NM', 'CMPLNT_FR_DT',
                 'CMPLNT_FR_TM', 'LAW_CAT_CD', 'LOC_OF_OCCUR_DESC',
                 'OFNS_DESC', 'PD_DESC', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX',
                 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX', 'X_COORD_CD', 'Y_COORD_CD',
                 'Latitude', 'Longitude']
    print(len(keep_cols))
    df[keep_cols].sample(2000).to_csv("../data/sample_data.csv")
    # for col in df.columns:
    #     miss_percent = df[col].isna().sum() / len(df[col])
    #     if miss_percent < 0.5:
    #         keep_cols.append(col)
    #
    # df[keep_cols].to_csv('../data/full_data.csv')
