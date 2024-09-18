import pandas as pd
import imf_datatools
import datetime
import time
import fadfpdata.myclass.dummy as dum
from fadfpdata.downloads import ecos_root

wo_aggregate = dum.Dummy().noagg

folder_vintage = f'{ecos_root}/WEOvintages'

vintagelist = [
    'WEO_WEOApr2000Pub',
    'WEO_WEOApr2001Pub',
    'WEO_WEOApr2002Pub',
    'WEO_WEOApr2003Pub',
    'WEO_WEOApr2004Pub',
    'WEO_WEOApr2005Pub',
    'WEO_WEOApr2006Pub',
    'WEO_WEOApr2007Pub',
    'WEO_WEOApr2008Pub',
    'WEO_WEOApr2009Pub',
    'WEO_WEOApr2010Pub',
    'WEO_WEOApr2011Pub',
    'WEO_WEOApr2012Pub',
    'WEO_WEOApr2013Pub',
    'WEO_WEOApr2014Pub',
    'WEO_WEOApr2015Pub',
    'WEO_WEOApr2016Pub',
    'WEO_WEOApr2017Pub',
    'WEO_WEOApr2018Pub',
    'WEO_WEOApr2019Pub',
    'WEO_WEOApr2020Pub',
    'WEO_WEOApr2021Pub',
    'WEO_WEOApr2022Pub',
    'WEO_WEOApr2023Pub',
    'WEO_WEOApr2024Pub',
]

varlist = [
    "ENDA",
    "ENDE",
    "GGCB",
    "GGCB_GDP",
    "GGCBP",
    "GGCBP_GDP",
    "GGEI",
    "GGEI_GDP",
    "GGR",
    "GGR_GDP",
    "GGX",
    "GGX_GDP",
    "GGXCNL",
    "GGXCNL_GDP",
    "GGXONLB",
    "GGXONLB_GDP",
    "GGXWDG",
    "GGXWDG_GDP",
    "GGDS",
    "NGDP",
    "NGDPD",
    "NGDP_FY",
    "NGDP_FY_USD"
]

# This process takes about 10-15min
def pull_vintage(var_list):
    starttime = time.time()

    df = pd.DataFrame()
    for database in vintagelist:
        print(database)
        dfweo = imf_datatools.get_ecos_sdmx_data(database, wo_aggregate, var_list, freq='A', longformat=True)
        if not isinstance(dfweo, pd.DataFrame):
            continue
        dfweo['vintage_year'] = int(database[10:14])
        df = pd.concat([df, dfweo], ignore_index=True)
        
    df['year'] = df['dates'].dt.year
    df.rename(columns={'COUNTRY': 'ifscode'}, inplace=True)
    df.columns = df.columns.str.lower().str.replace('.a', '', regex=False)
    df = df[['ifscode', 'vintage_year', 'year'] + [var.lower() for var in var_list]]

    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    df.to_csv(f'{folder_vintage}/WEOvintages_{timestamp}.csv', index=False)
    endtime = time.time()
    print(f'Download complete. Time Duration: {round((endtime-starttime)/60, 1)}min')


if __name__ == '__main__':
    # vintagelist = ['WEO_WEOApr2024Pub', 'WEO_WEOApr2024Pub']
    # varlist = ['GGR', 'GGX', 'GGEI', 'IAR_BP6', 'BMGS_BP6', 'NGDP']
    pull_vintage(varlist)
