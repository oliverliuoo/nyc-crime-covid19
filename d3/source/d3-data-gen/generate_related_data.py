"""Preprocess data to get related data map."""

import json

from typing import Dict, List, Tuple
import pandas as pd

CRIME_LIST = ['SEX CRIMES', 'ASSAULT', 'THEFT', 'ROBBERY', 'MURDER']
PRECINCT_LIST = [1, 5, 6, 7, 9, 10, 13, 14, 17, 18, 19, 20, 22, 23, 24, 25, 26, 28, 30, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 60, 61, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 75, 76, 77, 78, 79, 81, 83, 84, 88, 90, 94, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 120, 121, 122, 123]


def gen_map_nest2(row_map: Dict) -> Dict:
    res_dict = {}
    for key in row_map:
        key1, key2 = key
        if key1 not in res_dict:
            res_dict[key1] = {}
        res_dict[key1][key2] = row_map[key]

    return res_dict


def gen_map_nest3(row_map: Dict, unwrap_order: Tuple = (0, 1, 2)) -> Dict:
    res_dict = {}
    for key in row_map:
        key1, key2, key3 = key[unwrap_order[0]], key[unwrap_order[1]], key[unwrap_order[2]]
        if key1 not in res_dict:
            res_dict[key1] = {}
        if key2 not in res_dict[key1]:
            res_dict[key1][key2] = {}
        res_dict[key1][key2][key3] = row_map[key]

    return res_dict


def gen_map_nest3_new(row_map: Dict, unwrap_order: Tuple = (0, 1, 2)) -> Dict:
    def gen_counter(mode: int) -> Dict:
        if mode == 1:
            res = {precinct: {crime_type: 0 for crime_type in CRIME_LIST}
                   for precinct in PRECINCT_LIST}
        else:
            res = {crime_type: {precinct: 0 for precinct in PRECINCT_LIST}
                   for crime_type in CRIME_LIST}
        return res

    res_dict = {}
    for key in row_map:
        key1, key2, key3 = key[unwrap_order[0]], key[unwrap_order[1]], key[unwrap_order[2]]
        if key1 not in res_dict:
            counter = gen_counter(unwrap_order[1])
            res_dict[key1] = counter
        res_dict[key1][key2][key3] = row_map[key]

    return res_dict


def get_list_for_type(row_map: Dict) -> List:
    res_list = []
    nest_map = gen_map_nest2(row_map)
    for crime_type in nest_map:
        sum_cnt = sum(nest_map[crime_type].values())
        cur_dict = {'type': crime_type,
                    'cnt': sum_cnt,
                    'precinct_map': nest_map[crime_type]}
        res_list.append(cur_dict)

    return res_list


def get_list_for_other(row_map: Dict) -> List:
    res_list = []
    nest_map_1 = gen_map_nest3_new(row_map, unwrap_order=(0, 1, 2))
    nest_map_2 = gen_map_nest3_new(row_map, unwrap_order=(0, 2, 1))
    for key in nest_map_1:
        # get sum of count
        sum_cnt = 0
        for sub_key in nest_map_1[key]:
            sum_cnt += sum(nest_map_1[key][sub_key].values())

        cur_dict = {'type': key,
                    'cnt': sum_cnt,
                    'precinct_type_map': nest_map_1[key],
                    'type_precinct_map': nest_map_2[key]}
        res_list.append(cur_dict)

    return res_list


if __name__ == '__main__':
    df = pd.read_csv('../data/crime_data.csv')

    crime_list = pd.unique(df['crime_type'])
    precinct_list = sorted(pd.unique(df['arrest_precinct']))
    print(crime_list)
    print(precinct_list)
    # precinct
    precinct_type_row_map = df.groupby(['arrest_precinct',
                                       'crime_type'])['arrest_precinct']\
        .count().to_dict()
    cnt_group_by_precinct = gen_map_nest2(precinct_type_row_map)
    for key in cnt_group_by_precinct:
        cnt_group_by_precinct[key]['sum'] = sum(cnt_group_by_precinct[key].values())
    
    with open('../data/cnt_group_by_precinct.json', 'w') as f:
        json.dump(cnt_group_by_precinct, f)
    
    # crime type
    type_precinct_row_map = df.groupby(['crime_type',
                                        'arrest_precinct'])['crime_type']\
        .count().to_dict()
    
    data_for_crime_type = get_list_for_type(type_precinct_row_map)
    with open('../data/data_list_for_crime_type.json', 'w') as f:
        json.dump(data_for_crime_type, f)
    
    # criminal age group
    age_row_map = df.groupby(['age_group',
                             'arrest_precinct',
                              'crime_type'])['age_group'] \
        .count().to_dict()

    data_for_age_group = get_list_for_other(age_row_map)
    print(data_for_age_group)
    with open('../data/data_list_for_age_group.json', 'w') as f:
        json.dump(data_for_age_group, f)

    # criminal sex
    sex_row_map = df.groupby(['perp_sex',
                             'arrest_precinct',
                              'crime_type'])['perp_sex'] \
        .count().to_dict()

    data_for_perp_sex = get_list_for_other(sex_row_map)
    print(data_for_perp_sex)
    with open('../data/data_list_for_perp_sex.json', 'w') as f:
        json.dump(data_for_perp_sex, f)

    # criminal race
    race_row_map = df.groupby(['perp_race',
                              'arrest_precinct',
                               'crime_type'])['perp_race'] \
        .count().to_dict()

    data_for_perp_race = get_list_for_other(race_row_map)
    print(data_for_perp_race)
    with open('../data/data_list_for_perp_race.json', 'w') as f:
        json.dump(data_for_perp_race, f)
