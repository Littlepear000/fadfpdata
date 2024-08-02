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

data = ecos[['ifscode', 'year', 'ggei', 'ggxwdg', 'ngdp', 'ggxcnl_gdp']].query('year >= 2000')
data['g'] = data.groupby('ifscode')['ngdp'].pct_change()
data['ggxwdg_l'] = data.groupby('ifscode')['ggxwdg'].shift(1)
data['r'] = data['ggei'] / data['ggxwdg_l']
data['rlessg'] = (data['r'] - data['g'])/(1 + data['g']) *100


rlessg = data[(data['year']>=curr_year) & (data['year']<=curr_year+5)]
rlessg = rlessg.groupby('ifscode')['rlessg'].mean().reset_index()
rlessg['country'] = rlessg['ifscode'].map(ifs_to_countryname)