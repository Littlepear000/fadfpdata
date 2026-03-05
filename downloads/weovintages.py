import pandas as pd
import datetime
import time
import os
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.myclass.ImfFrame import ImfFrame
from fadfpdata.downloads import ecos_root

wo_aggregate = Dummy().noagg

folder_vintage = f'{ecos_root}/WEOvintages'
year_range = range(2000, 2026)
months = ['Jan', 'Apr', 'Jul', 'Oct']
vintagelist = []
for year in year_range:
    for month in months:
        vintagelist.append(f'WEO{month}{year}Pub')
vintagelist = vintagelist + ['WEOJan2026Pub']

varlist = [
    "ENDA",
    "ENDE",
    "GGCB",
    "GGCB_GDP",
    "GGCBP",
    "GGCBP_GDP",
    "GGE",
    "GGEI",
    "GGEI_GDP",
    "GGR",
    "GGR_GDP",
    "GGROPI",
    "GGX",
    "GGX_GDP",
    "GGXCNL",
    "GGXCNL_GDP",
    "GGXONLB",
    "GGXONLB_GDP",
    "GGXWDG",
    "GGXWDG_GDP",
    "NGDP",
    "NGDPD",
    "NGDP_FY",
    "NGDP_FY_USD",
    "GGDS",
    "LP",
    "NGDP_D",
    "PCPI",
    "NGDP_DPCH",
    "NGDP_RPCH",
    "PCPI_PCH",
    "GGECE",
    "GGEEC",
    "GGEGS",
    "GGES",
    "GGESS",
    "NFI",
    "GGAAN_T",
    "NGAP_R"
]

def pull_vintage():
    starttime = time.time()

    df = pd.DataFrame()
    for database in vintagelist:
        print(database)
        vintage_month = database[3:6]
        vintage_year = database[6:10]
        file_path = fr"\\data1\WEO\WEO_Stata_Databases\{database}.dta"

        if not os.path.exists(file_path):
            continue

        temp = pd.read_stata(fr"\\data1\WEO\WEO_Stata_Databases\{database}.dta")
        temp['vintage_year'] = vintage_year + vintage_month
        existing_vars = [v.lower() for v in varlist if v.lower() in temp.columns]
        temp = temp[['vintage_year', 'country', 'ifscode', 'year'] + existing_vars]
        df = pd.concat([df, temp], ignore_index=True)

    df['ifscode'] = pd.to_numeric(df['ifscode'], errors='coerce')
    df = df[~df['ifscode'].isna()]
    df['ifscode'] = df['ifscode'].astype(int)
    df = ImfFrame(df)

    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    for m in months:
        print(f'Exporting WEO {m} vintages...')
        df_m = df[df['vintage_year'].str.contains(m, na=False)]
        df_m.to_csv(f'{folder_vintage}/{m}/WEOvintages_{m}_{timestamp}.csv', index=False)
    endtime = time.time()
    print(f'Download complete. Time Duration: {round((endtime-starttime)/60, 1)}min')

# This process takes about 10-15min
# def pull_vintage_old(var_list):
#     starttime = time.time()
#
#     df = pd.DataFrame()
#     for database in vintagelist:
#         print(database)
#         vintage_month = database[7:10]
#         vintage_year = database[10:14]
#         dfweo = imf_datatools.get_ecos_sdmx_data(database, wo_aggregate, var_list, freq='A', longformat=True)
#         if not isinstance(dfweo, pd.DataFrame):
#             continue
#         dfweo['vintage_year'] = vintage_year + vintage_month
#         df = pd.concat([df, dfweo], ignore_index=True)
#
#     df['year'] = df['dates'].dt.year
#     df.rename(columns={'COUNTRY': 'ifscode'}, inplace=True)
#     df.columns = df.columns.str.lower().str.replace('.a', '', regex=False)
#     df = df[['ifscode', 'vintage_year', 'year'] + [var.lower() for var in var_list]]
#
#     timestamp = datetime.datetime.now().strftime('%Y%m%d')
#     df.to_csv(f'{folder_vintage}/WEOvintages_{timestamp}.csv', index=False)
#     endtime = time.time()
#     print(f'Download complete. Time Duration: {round((endtime-starttime)/60, 1)}min')


if __name__ == '__main__':
    # vintagelist = ['WEO_WEOApr2024Pub', 'WEO_WEOApr2024Pub']
    # varlist = ['GGR', 'GGX', 'GGEI', 'IAR_BP6', 'BMGS_BP6', 'NGDP']
    pull_vintage()
