import pandas as pd
import numpy as np
import pandaspro as cpd
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.myclass.idata import iData
from fadfpdata.utils.core import cname_to_ifs, ifs_to_cname, iso_to_ifs

fm_version = '2026-04'
fm_folder_name = 'April Monitor'
curr_year = int(fm_version[:4])
curr_mon = int(fm_version[-2:])
fm_folder = f'{fm_version}-{fm_folder_name}'
input_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA\input sources'
output_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA'
blmbg_update_date = '20260204'
wbnrh_update_date = '20260209'
weo_update_date = '20260209'
ep_update_date = '20260206'
ep_start_year = 2025

weodata = iData()
dum = Dummy()

col_ren = {
            'country': '',
            f'Y_{ep_start_year}_to_2030_pension': f'Pension Spending Change, {ep_start_year}–30',
            f'NPV{ep_start_year}_2050_pension': f'Net Present Value of Pension Spending Change, {ep_start_year}–50',
            f'Y_{ep_start_year}_to_2030_health': f'Health Care Spending Change, {ep_start_year}–30',
            f'NPV{ep_start_year}_2050_health': f'Net Present Value of Health Care Spending Change, {ep_start_year}–50',
            'gfn': 'Gross Financing Need, 2024',
            'years_to_maturity': 'Average Term to Maturity, 2024 (years)',
            'debt_to_maturity': 'Debt to Average Maturity, 2024',
            'rlessg': 'Projected Interest Rate–Growth Differential, 2024–29 (percent)',
            'pre_pan_cnl': 'Pre-Pandemic Overall Balance, 2012–19',
            'ggxcnl_gdp': 'Projected Overall Balance, 2024–29',
            'nrh': 'Nonresident Holding of General Government Debt, 2023 (percent of total)',
            'nfw': 'Net Financial Worth of General Government, 2021 (percent of GDP)'
        }