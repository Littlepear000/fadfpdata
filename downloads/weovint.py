import pandas as pd
from fadfpdata.downloads import ecos_root

df = pd.read_csv(fr'{ecos_root}\WEOvintages\WEOvintages_20241028.csv')
month_dict = {
    'Jan': '01',
    'Apr': '04',
    'Jul': '07',
    'Oct': '10'
}
vintages = df['vintage_year'].unique()
for v in vintages:
    vint_rename = v[:4] + month_dict[v[-3:]]
    df_v = df[df['vintage_year'] == v]
    df_v.to_csv(
        fr'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Databases\ECOS\WEOvint\WEOvint_{vint_rename}.csv',
        index=False)
