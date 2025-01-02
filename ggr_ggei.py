from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.utils.core import *
import pandaspro as cpd
from fadfpdata.myclass.ImfFrame import ImfFrame
from fadfpdata.myclass.weovint import WeoVint


# dum = Dummy()
# ecos = EcosData()
df_jul = WeoVint(version='202407')
varlist = [
    'ifscode', 'year', 'ngdpd', 'ngdp_fy', 'ggr_gdp', 'ggei_gdp', 'ggei',
    'ggr', 'ggropi', 'enda'
]
df = df_jul[varlist].query('year >= 2000')

# net income
# inc_dict2 = {
#     'United States': [111],
#     'G7': dum.g7,
# }
#
# df_sum = ImfFrame({'year': df['year'].unique()})
# for cgroup, clist in inc_dict.items():
#     group_sum = df.inlist('ifscode', clist).groupby('year')[['ggei_d', 'ggr_d']].sum(['ggei_d', 'ggr_d']).reset_index()
#     group_sum = group_sum.rename(columns={'ggei_d': f'{cgroup}_ggei_d', 'ggr_d': f'{cgroup}_ggr_d'})
#     df_sum = df_sum.merge(group_sum, on='year')
# final1 = ImfFrame(df).agg_mean('weov_multi_var_group_report', inc_dict, weight='ggr_d')
# final2 = ImfFrame(df).agg_mean('ggei_ggr_net', inc_dict2)
#
# ps = cpd.PutxlSet(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\2024OctFM_Figure 1.17-B Interest Payments to Revenues.xlsx')
# ps.putxl(df, sheet_name='raw_vintJul', cell='A1', header=True, index=False)
# ps.putxl(final1, sheet_name='chart_clean_vintJul', cell='A1', header=True, index=True)
# ps.putxl(final2, sheet_name='chart_clean_vintJul', cell='L1', header=True, index=False)

df.export_agg_detail(indicator='weov_multi_var_group_report',
                     excel_file=r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_Ad hoc\FADFP\202410 - Interest-to-revenue chart with different vintage\Interest-payment-to-revenue.xlsx',
                     sheet_name='with_median_vintJul',
                     start_cell='B2',
                     weight='ggr_d')