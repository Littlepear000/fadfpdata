from fadfpdata.fm import *
import numpy as np

# Gross financing needs: AE - source: Bloomberg + WEO
ddis = cpd.pwread(fr'{input_folder}/Bloomberg_DDIS_AE_{blmbg_update_date}.xlsx', sheet_name='Mat_Debt%', cellrange='B3:F36')[0]
ddis['ifscode'] = ddis['country'].map(cname_to_ifs)
for year in range(curr_year, curr_year+4):
    ddis[str(year)] = ddis[str(year)]*10**6
ddis = ddis.melt(id_vars=['country', 'ifscode'],
                 value_vars=[str(yr) for yr in list(range(curr_year, curr_year+4))],
                 var_name='year',
                 value_name='ddis')
ddis['year'] = ddis['year'].astype('int')
ddis = ddis.merge(weodata[['ifscode', 'year', 'ngdp_fy']], on=['ifscode', 'year'], how='left')
ddis['maturing_debt'] = ddis['ddis'] / ddis['ngdp_fy'] * 100
ddis_ae = ddis.inlist('year', curr_year)

deficit_ae = weodata.inlist('ifscode', dum.ae).inlist('year', curr_year)
deficit_ae['deficit'] = - deficit_ae['ggxcnl'] / deficit_ae['ngdp_fy'] * 100
gfn_ae = deficit_ae.merge(ddis_ae, on=['ifscode', 'year'], how='left')[['ifscode', 'deficit', 'maturing_debt']]

# Gross financing needs: EMDE - source: WEO
gfn_emde = weodata.inlist('ifscode', dum.emde).inlist('year', curr_year)
gfn_emde['deficit'] = - gfn_emde['ggxcnl'] / gfn_emde['ngdp_fy'] * 100
gfn_emde['maturing_debt'] = (gfn_emde['ggds'] - gfn_emde['ggei']) / gfn_emde['ngdp_fy'] * 100
gfn_emde = gfn_emde[['ifscode', 'deficit', 'maturing_debt']]

gfn = pd.concat([gfn_ae, gfn_emde]).sort_values('ifscode')

# Gross financing needs: source: additional amortization data from country desk
desk = cpd.pwread(fr'{input_folder}/Additional country desk data on amortization.xlsx')[0]
desk['ifscode'] = desk['country'].map(cname_to_ifs)
amort_map = desk.cpdmap_ifscode__amort
for ifs, amort in amort_map.items():
    gfn.loc[gfn['ifscode'] == ifs, 'maturing_debt'] = amort

gfn['gfn'] = gfn['deficit'] + gfn['maturing_debt']

# Countries to be excluded
hide_list = ['Andorra', 'Hong Kong', 'Israel', 'Luxembourg', 'Norway']
for country in hide_list:
    gfn.loc[gfn['ifscode'] == cname_to_ifs[country], 'gfn'] = np.nan
