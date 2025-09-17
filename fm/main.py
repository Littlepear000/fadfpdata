from fadfpdata.fm import *
from fadfpdata.fm.prep_ep import ep
from fadfpdata.fm.prep_cnl import cnl
from fadfpdata.fm.prep_gfn import gfn
from fadfpdata.fm.prep_rlessg import rlessg
from fadfpdata.fm.prep_to_maturity import d_to_m
from fadfpdata.fm.prep_non_resholding import nrh

def weighted_avg(group, indicator):
    group = group.dropna(subset=[indicator, 'ngdp_fy_usd'])
    return (group[indicator] * group['ngdp_fy_usd']).sum() / group['ngdp_fy_usd'].sum()

ngdpd_fy = ecos.query(f'year == {curr_year}')[['ifscode', 'ngdp_fy_usd']]
fix_col = pd.read_excel(fr'{input_folder}\fixed columns.xlsx', sheet_name='combine')
table = fix_col.copy()
for df in [ep, cnl, gfn, rlessg, d_to_m, nrh, ngdpd_fy]:
    table = table.merge(df, on='ifscode', how='left')
table = cpd.FramePro(table)

group_dict = {
    'AE': dum.ae,
    'EM': dum.em,
    'LIC': dum.lic,
    'G7': dum.g7,
    'G20': dum.g20,
    'G20_adv': dum.g20_adv,
    'G20_em': dum.g20_em
}
pre_pan_cnl_dict = {
    'AE': -3.1,
    'EM': -3.1,
    'LIC': -3.3,
    'G7': -4.0,
    'G20_adv': -3.6,
    'G20_em': -3.5
}

agg_all = pd.DataFrame()
for group in group_dict.keys():
    df_group = table.inlist('ifscode', group_dict[group])
    weighted_avg = {}
    for col in [col for col in df_group.columns if col not in ['country', 'ifscode', 'ngdpd_fy']]:
        weighted_avg[col] = (df_group[col] * df_group['ngdp_fy_usd']).sum() / df_group['ngdp_fy_usd'].sum()
    agg = pd.DataFrame(weighted_avg, index= [group])
    agg_all = pd.concat([agg_all, agg])

agg_all = agg_all.reset_index().rename(columns={'index': 'country'})
final_table = pd.concat([agg_all, table.drop('ifscode', axis=1)])[col_ren.keys()].reset_index().drop('index', axis=1).fillna('...')
final_table.loc[final_table['country'].isin(group_dict.keys()), 'nfw'] = ''
final_table.loc[final_table['country'].isin(pre_pan_cnl_dict.keys()), 'pre_pan_cnl'] = final_table['country'].map(pre_pan_cnl_dict)

stat23_25_dict = {
    'STAT23': 'B3:B42',
    'STAT24': 'B3:B47',
    'STAT25': 'B3:B43',
}

ps = cpd.PutxlSet(fr'{output_folder}\Stat_Tables23-25_FMOct2025_{weo_update_date}.xlsx')
for sheet, cellrange in stat23_25_dict.items():
    country_order = cpd.pwread(fr'{output_folder}\Stat_Tables23-25_FMOct2025_{weo_update_date}.xlsx', sheet_name=sheet, cellrange=cellrange)[0].rename(columns={'unnamed_1': 'country'})
    table_final = country_order.merge(final_table, on='country', how='left')
    ps.putxl(table_final.drop('country', axis=1), sheet_name=sheet, cell='C4', header=False, index=False)
