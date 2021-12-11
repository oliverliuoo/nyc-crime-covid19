"""Re-categorize data."""
import numpy as np
import pandas as pd


def crime_classifier(crime_name: str) -> str:
    if not isinstance(crime_name, str):
        return 'UNKNOWN'

    elif any(x in crime_name for x in ['LARCENY', 'STOLEN', 'BURGLAR', 'THEFT']):
        return 'THEFT'

    elif any(x in crime_name for x in ['ASSAULT', 'OFFENSES', 'OFF. AGNST']):
        return 'ASSAULT'

    elif any(x in crime_name for x in ['ROBBERY']):
        return 'ROBBERY'

    elif any(x in crime_name for x in ['RAPE', 'SEX']):
        return 'SEX CRIMES'

    elif any(x in crime_name for x in ['MURDER', 'HOMICIDE']):
        return 'MURDER'

    else:
        return 'OTHERS'


def loc_classifier(loc: str) -> str:
    if not isinstance(loc, str):
        return 'UNKNOWN'

    elif any(x in loc for x in ['STREET']):
        return 'STREET'

    elif any(x in loc for x in ['RESIDENCE']):
        return 'RESIDENCE'

    elif any(x in loc for x in ['STORE', 'COMMERCIAL', 'GROCERY',
                                'CLOTHING', 'MARKET', 'MERCHANT', 'LAUNDRY']):
        return 'RETAIL'

    elif any(x in loc for x in ['RESTAURANT', 'HOTEL', 'FAST', 'BAR']):
        return 'RECREATION'

    elif any(x in loc for x in ['TRANSIT', 'BUS', 'TAXI', 'TERMINAL']):
        return 'TRANSPORTATION'

    elif any(x in loc for x in ['PARK', 'HOMELESS']):
        return 'OPEN SPACE'

    else:
        return 'OTHERS'


if __name__ == '__main__':
    raw_data = pd.read_csv('../data/crime_data.csv')
    classified_crime_series = raw_data['OFNS_DESC'].apply(crime_classifier)
    classified_loc_series = raw_data['PREM_TYP_DESC'].apply(loc_classifier)
    raw_data['CRIME_CAT'] = classified_crime_series
    raw_data['LOC_CAT'] = classified_loc_series
    raw_data.to_csv('../data/crime_data_new.csv')
