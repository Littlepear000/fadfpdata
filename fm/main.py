import pandas as pd
import pandaspro as cpd
import sprnldata as spr
from imf_datatools import worldbank_utilities, edi_utilities
from sprnldata.utils.core import countryname_to_ifs, ifs_to_countryname
from sprnldata.myclass.dummy import Dummy

fm_version = '2024-10'
curr_year = int(fm_version[:4])
fm_folder = f'{fm_version}-October_Monitor' if fm_version[-2:]=='10' else f'{fm_version}-April_Monitor'
input_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA\input sources'
weo_version = 'WEO_WEOJul2024Pub'
blmbg_update_date = '20240718'
ecos = spr.ecos()
dum = Dummy()


# Average term to maturity - source: Bloomberg
maturity_raw = cpd.pwread(fr'{input_folder}/Bloomberg_Years_to_Maturity_{blmbg_update_date}.xlsx', sheet_name=blmbg_update_date, cellrange='H:I')[0].drop(0)
maturity_raw.columns = ['country', 'years_to_maturity']
maturity_raw['ifscode'] = maturity_raw['country'].map(countryname_to_ifs)
maturity = maturity_raw.dropna(subset='ifscode')[['ifscode', 'years_to_maturity']]

# Debt to average maturity - source: Bloomberg + WEO
weodata = imf_datatools.get_ecos_sdmx_data(weo_version, 'all', ['GGXWDG_GDP'], freq='A', longformat=True)
weolivedata = imf_datatools.get_ecos_sdmx_data('WEO_WEO_Live', 'all', ['GGXWDG_GDP'], freq='A', longformat=True)

weodata.columns = ['ifscode', 'dates', 'ggxwdg_gdp']
weodata['year'] = weodata['dates'].dt.year
weodata = weodata[weodata['year']==int(fm_version[:4])-1]





# data = pd.read_csv(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Databases\ECOS\Ecos\ecosdata_20240703.csv')[['ifscode', 'year', 'ggei', 'ggxwdg', 'ngdp']]
data = imf_datatools.get_ecos_sdmx_data(weo_version, 'all', ['GGEI', 'GGXWDG', 'NGDP', 'GGXCNL_GDP'], freq='A', longformat=True)
data.columns = data.columns.str.lower()
data['year'] = data['dates'].dt.year
data = data.query('year >= 2000')
data['g'] = data.groupby('ifscode')['ngdp'].pct_change()
data['ggxwdg_l'] = data.groupby('ifscode')['ggxwdg'].shift(1)
data['r'] = data['ggei'] / data['ggxwdg_l']
data['rlessg'] = (data['r'] - data['g'])/(1 + data['g'])


# Non-resident holding
series = 'DT.DOD.DECT.CD.GG.AR.US'
# Get all metadata
meta = worldbank_utilities.get_all_worldbank_metadata()
# Check the series of interest is available
series in meta.index

# Get the data for all available countries
wbdata = worldbank_utilities.get_worldbank_data(series, 'all', longformat=True)


