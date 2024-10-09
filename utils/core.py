import datetime
import os
import re
import pandas as pd
from fadfpdata import onedrive_root

countrycode_file = fr'{onedrive_root}\0_tools\Country Code & Template\Country Code & Grouping\Country Codes.xlsx'
country_name2code = pd.read_excel(countrycode_file, sheet_name='name_to_code')
country_name2code.loc[country_name2code['ifscode'] == 728, 'iso2'] = 'NA'
cname_to_ifs = {row['country']: int(row['ifscode']) for index, row in country_name2code.iterrows()}
countryname_to_iso = {row['country']: row['iso3'] for index, row in country_name2code.iterrows()}
countryname_to_iso2 = {row['country']: row['iso2'] for index, row in country_name2code.iterrows()}

country_code2name = pd.read_excel(countrycode_file, sheet_name='code_to_name')
country_code2name.loc[country_code2name['ifscode'] == 728, 'iso2'] = 'NA'
ifs_to_iso = {int(row['ifscode']): row['iso3'] for index, row in country_code2name.iterrows()}
iso_to_ifs = {row['iso3']: int(row['ifscode']) for index, row in country_code2name.iterrows() if row['iso3'] is not None}
iso2_to_ifs = {row['iso2']: int(row['ifscode']) for index, row in country_code2name.iterrows() if row['iso2'] is not None}
ifs_to_countryname = {int(row['ifscode']): row['country'] for index, row in country_code2name.iterrows()}
iso_to_countryname = {row['iso3']: row['country'] for index, row in country_code2name.iterrows()}
iso2_to_countryname = {row['iso2']: row['country'] for index, row in country_code2name.iterrows()}

def get_latest_file(folder_path, debug=False):
    files = os.listdir(folder_path)
    if debug:
        print(files)
    timelist = []
    # print(files)
    for file in files:
        if file.endswith('.csv') or file.endswith('.xlsx'):
            if re.search(r'\d{8}', file):
                timestamp = datetime.datetime.strptime(re.findall(r'\d{8}', file)[0], '%Y%m%d')
                timelist.append(timestamp)
    max_time = max(timelist).strftime('%Y%m%d')
    return max_time

def weighted_avg(df, indicator):
    df = df.dropna(subset=[indicator, 'ngdpd'])
    df_weighted = (df[indicator] * df['ngdpd']).sum() / df['ngdpd'].sum()
    return df_weighted
