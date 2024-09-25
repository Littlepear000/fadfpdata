import pandas as pd
import numpy as np
import os
import re
import pandaspro as cpd
from pandaspro import FramePro
import fadfpdata as fad
from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.myclass.weovintage import WeoVinage

def weighted_avg(group):
    group = group.dropna(subset=['ggxwdg_gdp', 'ngdpd'])
    return (group['ggxwdg_gdp'] * group['ngdpd']).sum() / group['ngdpd'].sum()

ecos = EcosData()[['ifscode', 'year', 'ggxwdg_gdp', 'ngdpd']].query('year >= 2000')
ecos_wide = ecos.pivot(index='ifscode',
                       columns='year',
                       values='ggxwdg_gdp').reset_index()
ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Fiscal Monitor October 2024\Charts and figures\Figure 1.1. Public Debt to GDP ratio, 2000-29.xlsx')
ps.putxl(temp.drop('year', axis=1), sheet_name='C_GLOBAL', cell='U7', index=False, header=False)

ecos = ecos[~ecos['ifscode'].isin([111, 924])]
weovint = WeoVinage().v2010[['ifscode', 'year', 'ggxwdg_gdp', 'ngdpd']]

temp = ecos.groupby('year').apply(weighted_avg).reset_index()
ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Fiscal Monitor October 2024\Charts and figures\Figure 1.1. Public Debt to GDP ratio, 2000-29.xlsx')
ps.putxl(temp.drop('year', axis=1), sheet_name='C_GLOBAL', cell='U7', index=False, header=False)

countrydummy_file = 'xldummies.xlsx'

# Country lists
w_aggregate = FramePro(pd.read_excel(countrydummy_file)).inlist('w_aggregate', 1)['ifscode'].tolist()
wo_aggregate = FramePro(pd.read_excel(countrydummy_file)).inlist('wo_aggregate', 1)['ifscode'].tolist()

res_weovintage_folder = r'\\data1\WEO\WEO_Stata_Databases'
files = os.listdir(res_weovintage_folder)
apr_vintages = [f for f in files if 'WEOApr' in f and 'PubQ' not in f ]

df = pd.DataFrame()

for year in range(2014, 2025):
    print(year)
    if year == 2024:
        dfvint = pd.read_stata(fr'{res_weovintage_folder}\WEOApr{year}Pub.dta')
        dfvint['vintage'] = f'Apr{year}'
    else:
        dfvint = pd.read_stata(fr'{res_weovintage_folder}\WEOOct{year}Pub.dta')
        dfvint['vintage'] = f'Oct{year}'

    dfvint = dfvint[dfvint['ifscode'].isin(wo_aggregate)][dfvint['year'] >= 2000]
    df = pd.concat([df, dfvint], ignore_index=True)

result = df.groupby(['vintage', 'year']).apply(weighted_avg).reset_index().pivot(index='vintage',
                                                                                 columns='year',
                                                                                 values=0)
apr2024_y2000 = result.loc['Apr2024', 2000]


df2007 = pd.read_stata(fr'{res_weovintage_folder}\WEOOct2007Pub.dta')
df2007['ggxwdg_gdp'] = df2007['ggd'] / df2007['ngdp'] * 100
df2007 = df2007[df2007['ifscode'].isin(wo_aggregate)][df2007['year']>=2000]
df2007['vintage'] = 'Oct2007'
result2007 = df2007.groupby(['vintage', 'year']).apply(weighted_avg).reset_index().pivot(index='vintage',
                                                                                 columns='year',
                                                                                 values=0)

final = pd.concat([result,result2007])
ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Charts and figures\Global Debt to GDP chart.xlsx')
# ps.putxl(final, 'data_manual', 'A1', index=True)