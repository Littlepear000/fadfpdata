import pandas as pd
import numpy as np
import os
import re
import pandaspro as cpd
from pandaspro import FramePro

def weighted_avg(group):
    return (group['ggxwdg_gdp'] * group['ngdpd']).sum() / group['ngdpd'].sum()

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

    dfvint = dfvint[dfvint['ifscode'].isin(wo_aggregate)][dfvint['year']>=2000]
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
ps.putxl(final, 'data_manual', 'A1', index=True)