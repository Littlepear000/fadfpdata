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
weo_debt = ecos[['ifscode', 'year', 'ggxwdg_gdp']].inlist('year', curr_year-1)
d_to_m = maturity.merge(weo_debt, on='ifscode', how='left')
d_to_m['debt_to_maturity'] = d_to_m['ggxwdg_gdp'] / d_to_m['years_to_maturity']
d_to_m['country'] = d_to_m['ifscode'].map(ifs_to_countryname)