import pandas as pd
import numpy as np
import pandaspro as cpd
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.utils.core import cname_to_ifs, ifs_to_countryname, iso_to_ifs

fm_version = '2024-10'
curr_year = int(fm_version[:4])
curr_mon = int(fm_version[-2:])
fm_folder = f'{fm_version}-October_Monitor' if curr_mon == 10 else f'{fm_version}-April_Monitor'
input_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA\input sources'
output_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA'
blmbg_update_date = '20241008'
weo_update_date = '20241009'

ecos = EcosData()
dum = Dummy()

col_ren = {
    'country': '',
    'Y_2023_to_2030_pension': 'Pension Spending Change, 2023–30',
    'NPV2023_2050_pension': 'Net Present Value of Pension Spending Change, 2023–50',
    'Y_2023_to_2030_health': 'Health Care Spending Change, 2023–30',
    'NPV2023_2050_health': 'Net Present Value of Health Care Spending Change, 2023–50',
    'gfn': 'Gross Financing Need, 2024',
    'years_to_maturity': 'Average Term to Maturity, 2024 (years)',
    'debt_to_maturity': 'Debt to Average Maturity, 2024',
    'rlessg': 'Projected Interest Rate–Growth Differential, 2024–29 (percent)',
    'pre_pan_cnl': 'Pre-Pandemic Overall Balance, 2012–19',
    'ggxcnl_gdp': 'Projected Overall Balance, 2024–29',
    'nrh': 'Nonresident Holding of General Government Debt,  2023 (percent of total)',
    'nfw': 'Net Financial Worth of General Government, 2021 (percent of GDP)'
}