import numpy as np
from fadfpdata.fm import *
from fadfpdata.myclass.nrh import Nrh

wbdata = Nrh(version=wbnrh_update_date)
wbdata = wbdata[(wbdata['dates'] >= f'{curr_year-1}-{curr_mon}-01') & (wbdata['ext_debt'].notnull())]
wbdata = wbdata.loc[wbdata.groupby(['iso', 'ifscode'])['dates'].idxmax()]
nrh = ecos[['ifscode', 'year', 'ggxwdg', 'ende']].merge(wbdata, on=['ifscode', 'year'], how='right')
nrh['nrh'] = nrh['ext_debt'] * nrh['ende'] / nrh['ggxwdg'] * 100
nrh = nrh[['ifscode', 'nrh']]

## Manual changes
nrh.loc[nrh['ifscode'] == 622, 'nrh'] = np.nan  # Cameroon excluded due to large drop, country team still investigating
