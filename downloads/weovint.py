import pandas as pd
from fadfpdata.downloads import ecos_root
from fadfpdata.utils.core import get_latest_file
import os

month_dict = {
    'Jan': '01',
    'Apr': '04',
    'Jul': '07',
    'Oct': '10'
}

all_vintages = pd.DataFrame()
for month in month_dict.keys():
    print(month)
    vintages_folder = fr'{ecos_root}\WEOvintages'
    latest_date = get_latest_file(fr'{vintages_folder}\{month}')
    df = pd.read_csv(fr'{vintages_folder}\{month}\WEOvintages_{month}_{latest_date}.csv')
    all_vintages = pd.concat([all_vintages, df])

vintages = all_vintages['vintage_year'].unique()
for v in vintages:
    vint_rename = v[:4] + month_dict[v[-3:]]
    output_path = fr'{ecos_root}\WEOvint\WEOvint_{vint_rename}.csv'
    # if os.path.exists(output_path):
    #     continue
    print(vint_rename)
    df_v = all_vintages[all_vintages['vintage_year'] == v]
    df_v.to_csv(output_path, index=False)