import datetime
import os
import re
import numpy as np
import pandas as pd
from fadfpdata import onedrive_root
from fadfpdata.myclass.dummy import Dummy

dum = Dummy()
inc_dict = {
    'Global': dum.noagg,
    'Advanced Economies': dum.ae,
    'Emerging Market': dum.em,
    'Low-Income Developing Markets': dum.lic,
    'Emerging Market and Developing Economies': dum.emde,
    'Emerging Market and Developing Economies excl. China': dum.emde_nochina,
    'Advanced Economies excl. US': dum.ae_nous,
    'Emerging Market excl. China': dum.em_nochina,
    'United States': [111],
    'China': [924]
}

weo_countrycode_file = fr'{onedrive_root}\0_tools\Country Code & Template\Country Code & Grouping\Country Codes.xlsx'
country_name2code = pd.read_excel(weo_countrycode_file, sheet_name='name_to_code')
country_name2code.loc[country_name2code['ifscode'] == 728, 'iso2'] = 'NA'
fm_countrycode_file = None
cname_to_ifs = {row['country']: int(row['ifscode']) for index, row in country_name2code.iterrows() if not pd.isna(row['ifscode'])}
cname_to_iso = {row['country']: row['iso3'] for index, row in country_name2code.iterrows()}
cname_to_iso2 = {row['country']: row['iso2'] for index, row in country_name2code.iterrows()}

country_code2name = pd.read_excel(weo_countrycode_file, sheet_name='code_to_name')
country_code2name.loc[country_code2name['ifscode'] == 728, 'iso2'] = 'NA'
ifs_to_iso = {int(row['ifscode']): row['iso3'] for index, row in country_code2name.iterrows()}
iso_to_ifs = {row['iso3']: int(row['ifscode']) for index, row in country_code2name.iterrows() if row['iso3'] is not None}
iso2_to_ifs = {row['iso2']: int(row['ifscode']) for index, row in country_code2name.iterrows() if row['iso2'] is not None}
ifs_to_cname = {int(row['ifscode']): row['country'] for index, row in country_code2name.iterrows()}
iso_to_cname = {row['iso3']: row['country'] for index, row in country_code2name.iterrows()}
iso2_to_cname = {row['iso2']: row['country'] for index, row in country_code2name.iterrows()}

weo_group_code = pd.read_excel(weo_countrycode_file, sheet_name='weo_group_code')
gr_ifs_to_iso = {int(row['ifscode']): row['iso'] for index, row in weo_group_code.iterrows()}
gr_iso_to_ifs = {row['iso']: int(row['ifscode']) for index, row in weo_group_code.iterrows() if row['iso'] is not None}
gr_ifs_to_cname = {int(row['ifscode']): row['group'] for index, row in weo_group_code.iterrows()}
gr_iso_to_cname = {row['iso']: row['group'] for index, row in weo_group_code.iterrows()}


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

def weighted_avg(df, indicator, weight='ngdpd'):
    df = df.dropna(subset=[indicator, weight])
    weight_sum = df[weight].sum()
    if weight_sum == 0:
        return np.nan
    df_weighted = (df[indicator] * df[weight]).sum() / weight_sum
    return df_weighted


if __name__ == '__main__':
    # Sample data to test the weighted_avg function
    data = {
        'indicator': [5.5, 7.2, 6.8, None, 8.1],
        'ngdpd': [300, 450, 500, 200, 600]
    }

    # Create DataFrame
    df_sample = pd.DataFrame(data)
    test = df_sample.apply(lambda x: weighted_avg())
