from imf_datatools import worldbank_utilities
from fadfpdata.utils.core import iso_to_ifs
from fadfpdata import database_root
from pandaspro.core.tools.corder import corder
import datetime

# meta = worldbank_utilities.get_all_worldbank_metadata()
series = 'DT.DOD.DECT.CD.GG.AR.US'
date = datetime.datetime.today().strftime('%Y%m%d')
nrh = worldbank_utilities.get_worldbank_data(series, 'all', longformat=True).rename(columns={
    'countrycode': 'iso', 'countryname': 'country', 'DT.DOD.DECT.CD.GG.AR.US': 'ext_debt'
})

nrh.loc[nrh['iso'] == 'XKX', 'iso'] = 'KOS'
nrh.loc[nrh['iso'] == 'PSE', 'iso'] = 'WBG'
nrh['ifscode'] = nrh['iso'].map(iso_to_ifs)
nrh['year'] = nrh['dates'].dt.year
nrh = corder(nrh, ['country', 'iso', 'ifscode', 'year'])

nrh.to_csv(fr'{database_root}/NRH/nrh_{date}.csv', index=False)