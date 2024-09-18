from fadfpdata.fm import *
from imf_datatools import worldbank_utilities

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

wbdata = wbdata[(wbdata['dates'] >= f'{curr_year-1}-{curr_mon}-01') & (wbdata['ext_debt'].notnull())]
wbdata = wbdata.loc[wbdata.groupby(['iso', 'ifscode'])['dates'].idxmax()]
nrh = ecos[['ifscode', 'year', 'ggxwdg', 'ende']].merge(wbdata, on=['ifscode', 'year'], how='right')
nrh['nrh'] = nrh['ext_debt'] * nrh['ende'] / nrh['ggxwdg'] * 100
nrh = nrh[['ifscode', 'nrh']]
