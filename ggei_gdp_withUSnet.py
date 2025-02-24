import pandas as pd
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.utils.core import *
import pandaspro as cpd
from pandaspro import CellPro
from fadfpdata.myclass.ImfFrame import ImfFrame
from fadfpdata.myclass.weovint import WeoVint

# def weighted_avg(group, indicator):
#     group = group.dropna(subset=[indicator, 'ngdpd'])
#     return (group[indicator] * group['ngdpd']).sum() / group['ngdpd'].sum()

dum = Dummy()
ecos = EcosData()
res_weovintage_folder = r'\\data1\WEO\WEO_Stata_Databases'
# df_jul = ImfFrame(pd.read_stata(fr'{res_weovintage_folder}\WEOJul2024Pub.dta'))
df_jul = WeoVint(version='202407')
df = df_jul[['ifscode', 'year', 'ngdpd', 'ngdp_fy', 'ggr_gdp', 'ggei_gdp', 'ggei', 'ggr', 'ggropi', 'enda']].query('year >= 2000')
df['ggr_d'] = df['ggr'] / df['enda']
df['ggei_d'] = df['ggei'] / df['enda']

df['ggei_ggr'] = df['ggei'] / df['ggr'] * 100
df['ggei_ggr_net'] = (df['ggei'] - df['ggropi']) / df['ggr'] * 100

inc_dict2 = {
    'United States': [111],
    'G7': dum.g7,
}

df_sum = ImfFrame({'year': df['year'].unique()})
for cgroup, clist in inc_dict.items():
    group_sum = df.inlist('ifscode', clist).groupby('year')[['ggei_d', 'ggr_d']].sum(['ggei_d', 'ggr_d']).reset_index()
    group_sum = group_sum.rename(columns={'ggei_d': f'{cgroup}_ggei_d', 'ggr_d': f'{cgroup}_ggr_d'})
    df_sum = df_sum.merge(group_sum, on='year')
final1 = ImfFrame(df).agg_mean('ggei_ggr', inc_dict, weight='ggr_d')
final2 = ImfFrame(df).agg_mean('ggei_ggr_net', inc_dict2)

ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\2024OctFM_Figure 1.17-B Interest Payments to Revenues.xlsx')
ps.putxl(df, sheet_name='raw_vintJul', cell='A1', header=True, index=False)
ps.putxl(final1, sheet_name='chart_clean_vintJul', cell='A1', header=True, index=True)
ps.putxl(final2, sheet_name='chart_clean_vintJul', cell='L1', header=True, index=False)

df.export_agg_detail(indicator='ggei_ggr',
                     excel_file=r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\Interest-payment-to-revenue.xlsx',
                     sheet_name='with_median_vintJul',
                     start_cell='B2',
                     weight='ggr_d')