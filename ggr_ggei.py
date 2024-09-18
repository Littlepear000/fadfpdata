import pandas as pd
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.myclass.ecosdata import EcosData
import pandaspro as cpd
from pandaspro import CellPro

# def weighted_avg(group, indicator):
#     group = group.dropna(subset=[indicator, 'ngdpd'])
#     return (group[indicator] * group['ngdpd']).sum() / group['ngdpd'].sum()

dum = Dummy()
ecos = EcosData()

df = ecos[['ifscode', 'year', 'ngdpd', 'ggr', 'ggei']].query('year >= 2000')
df['ggei_ggr'] = df['ggei'] / df['ggr'] * 100

inc_dict = {
    'Global': dum.noagg,
    'Advanced Economies': dum.ae,
    'Emerging Market and Developing Economies': dum.emde,
}

final = df.create_aggregate('ggei_ggr', inc_dict)
ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Fiscal Monitor October 2024\Charts and figures\Figure 1.17-B Interest Payments to Revenues.xlsx')
ps.putxl(final, sheet_name='chart_clean', cell='A1', header=True, index=True)


eu_group_dict = {
    'Advanced Europe': dum.adv_eur,
    'Emerging Europe': dum.em_eur,
    'Emerging Europe excl. Russia': dum.emeur_norussia
}


#### Needs to follow up：封装到ImfFrame方法中
##########################################
output = pd.DataFrame()
ps = cpd.PutxlSet('FM_Figure 1.17-B Interest Payments to Revenues.xlsx')
ps.tab('ggei_ggr_EU')
start_cell = 'B2'
direction = 'right'

for group, list in eu_group_dict.items():

    filtered_df = df[df['ifscode'].isin(eu_group_dict[group])]
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
        start_cell = CellPro(ps.next_cell_right).offset(0, 2).cell
    elif direction == 'down':
        start_cell = CellPro(ps.next_cell_down).offset(3, 0).cell

ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202408 - Formating charts for FDMD presentation\FM_Figure 1.17-B Interest Payments to Revenues.xlsx')
ps.putxl(final, sheet_name='ggei_ggr_EU', cell='A1', index=False)