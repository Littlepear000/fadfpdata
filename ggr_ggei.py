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

temp_dict = {'LIC': dum.lic}
temp_final1 = (
    df.inlist('ifscode', dum.lic).dropna(subset=['ggei_d', 'ggr_d']).groupby('year')
    .agg(ggei_sum=('ggei_d', 'sum'), ggr_sum=('ggr_d', 'sum'))
    .assign(ratio=lambda x: x['ggei_sum'] / x['ggr_sum'] * 100)
)
temp_final2 = df.agg_mean('ggei_ggr', weight='ggr_d')
df.inlist('ifscode', dum.em_nochina).inlist('year', 2029).to_excel('temp2.xlsx')

inc_dict2 = {
    'United States': [111],
    'G7': dum.g7,
}

df_sum = ImfFrame({'year': df['year'].unique()})
for cgroup, clist in temp_dict.items():
    group_sum = df.inlist('ifscode', clist).groupby('year')[['ggei_d', 'ggr_d']].sum(['ggei_d', 'ggr_d']).reset_index()
    group_sum = group_sum.rename(columns={'ggei_d': f'{cgroup}_ggei_d', 'ggr_d': f'{cgroup}_ggr_d'})
    df_sum = df_sum.merge(group_sum, on='year')
final = ImfFrame(df).agg_mean('ggei_ggr', temp_dict, weight='ggr_d')

ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\2024OctFM_Figure 1.17-B Interest Payments to Revenues.xlsx')
ps.putxl(df, sheet_name='raw_vintJul', cell='A1', header=True, index=False)
ps.putxl(final, sheet_name='chart_clean_vintJul', cell='A1', header=True, index=True)

final = ImfFrame(df).agg_mean('ggei_ggr_net', inc_dict2)
# ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\2024OctFM_Figure 1.17-B Interest Payments to Revenues.xlsx')
ps.putxl(final, sheet_name='chart_clean_vintJul', cell='I1', header=True, index=False)

# ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\Interest-payment-to-revenue.xlsx')
# ps.putxl(final, sheet_name='chart_clean_vintJul', cell='A1', header=True, index=True)

# eu_group_dict = {
#     'Advanced Europe': dum.adv_eur,
#     'Emerging Europe': dum.em_eur,
#     'Emerging Europe excl. Russia': dum.emeur_norussia
# }


#### Needs to follow up：封装到ImfFrame方法中
##########################################
output = pd.DataFrame()
ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\Interest-payment-to-revenue.xlsx')
ps.tab('with_median_vintJul')
start_cell = 'B2'
direction = 'right'

for group, list in inc_dict.items():

    filtered_df = df[df['ifscode'].isin(list)]
    result = filtered_df.groupby('year').agg(
                mean=('ggei_ggr', 'mean'),
                weighted_avg=('ggei_ggr', lambda x: weighted_avg(filtered_df.loc[x.index], 'ggei_ggr')),
                median=('ggei_ggr', 'median'),
                p25=('ggei_ggr', lambda x: x.quantile(0.25)),
                p75=('ggei_ggr', lambda x: x.quantile(0.75)),
                p10=('ggei_ggr', lambda x: x.quantile(0.1)),
                p90=('ggei_ggr', lambda x: x.quantile(0.9)),
            ).reset_index()
    result['interquartile'] = result['p75'] - result['p25']
    result['10-90th'] = result['p90'] - result['p10']

    result_copy = cpd.FramePro(result.copy())
    result_copy['group'] = group
    result_copy = result_copy.corder('group')
    output = pd.concat([output, result_copy])

    ps.putxl(group, cell=CellPro(start_cell).offset(-1, 0).cell)
    ps.putxl(result, cell=start_cell, index=False)
    if direction == 'right':
        start_cell = CellPro(ps.next_cell_right.cell).offset(0, 2).cell
    elif direction == 'down':
        start_cell = CellPro(ps.next_cell_down.cell).offset(3, 0).cell