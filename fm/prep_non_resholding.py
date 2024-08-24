import pandas as pd
import pandaspro as cpd
import sprnldata as spr
from imf_datatools import worldbank_utilities, edi_utilities
from sprnldata.utils.core import iso_to_ifs
from sprnldata.myclass.dummy import Dummy

fm_version = '2024-10'
curr_year = int(fm_version[:4])
curr_mon = int(fm_version[-2:])
fm_folder = f'{fm_version}-October_Monitor' if fm_version[-2:]=='10' else f'{fm_version}-April_Monitor'
input_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA\input sources'
weo_version = 'WEO_WEOJul2024Pub'
blmbg_update_date = '20240718'
ecos = spr.ecos()
dum = Dummy()

# Non-resident holding
# meta = worldbank_utilities.get_all_worldbank_metadata()
series = 'DT.DOD.DECT.CD.GG.AR.US'
wbdata = worldbank_utilities.get_worldbank_data(series, 'all', longformat=True).rename(columns={
    'countrycode': 'iso', 'countryname': 'country', 'DT.DOD.DECT.CD.GG.AR.US': 'ext_debt'
})

wbdata.loc[wbdata['iso']=='XKX', 'iso'] = 'KOS'
wbdata.loc[wbdata['iso']=='PSE', 'iso'] = 'WBG'
wbdata['ifscode'] = wbdata['iso'].map(iso_to_ifs)
wbdata['year'] = wbdata['dates'].dt.year

wbdata = wbdata[(wbdata['dates'] > f'{curr_year-1}-{curr_mon}-01') & (wbdata['ext_debt'].notnull())]
wbdata = wbdata.loc[wbdata.groupby(['iso', 'ifscode'])['dates'].idxmax()]



