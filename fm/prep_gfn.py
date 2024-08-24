import pandas as pd
import pandaspro as cpd
import sprnldata as spr
from sprnldata.utils.core import countryname_to_ifs, ifs_to_countryname
from sprnldata.myclass.dummy import Dummy

fm_version = '2024-10'
curr_year = int(fm_version[:4])
fm_folder = f'{fm_version}-October_Monitor' if fm_version[-2:]=='10' else f'{fm_version}-April_Monitor'
input_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA\input sources'
blmbg_update_date = '20240718'
ecos = spr.ecos()
dum = Dummy()

# Gross financing needs: AE - source: Bloomberg + WEO
ddis = cpd.pwread(fr'{input_folder}/Bloomberg_DDIS_AE_{blmbg_update_date}.xlsx', sheet_name='Mat_Debt%', cellrange='B3:F36')[0]
ddis['ifscode'] = ddis['country'].map(countryname_to_ifs)
for year in range(curr_year, curr_year+4):
    ddis[str(year)] = ddis[str(year)]*10**6
ddis = ddis.melt(id_vars=['country', 'ifscode'],
                 value_vars=[str(yr) for yr in list(range(curr_year, curr_year+4))],
                 var_name='year',
                 value_name='ddis')
ddis['year'] = ddis['year'].astype('int')
ddis = ddis.merge(ecos[['ifscode', 'year', 'ngdp']], on=['ifscode', 'year'], how='left')
ddis['maturing_debt'] = ddis['ddis'] / ddis['ngdp'] *100
ddis_ae = ddis.inlist('year', curr_year)

deficit_ae = ecos.inlist('ifscode', dum.ae).inlist('year', curr_year)
deficit_ae['deficit'] = - deficit_ae['ggxcnl'] / deficit_ae['ngdp_fy'] * 100
gfn_ae = deficit_ae.merge(ddis_ae, on=['ifscode', 'year'], how='left')[['country', 'ifscode', 'year', 'deficit', 'maturing_debt']]
gfn_ae['gfn'] = gfn_ae['deficit'] + gfn_ae['maturing_debt']

# Gross financing needs: EMDE - source: WEO
gfn_emde = ecos.inlist('ifscode', dum.emde).inlist('year', curr_year)
gfn_emde['deficit'] = - gfn_emde['ggxcnl'] / gfn_emde['ngdp_fy'] * 100
gfn_emde['maturing_debt'] = (gfn_emde['ggds'] - gfn_emde['ggei']) / gfn_emde['ngdp_fy'] * 100
gfn_emde['gfn'] = gfn_emde['deficit'] + gfn_emde['maturing_debt']
gfn_emde = gfn_emde[['ifscode', 'year', 'deficit', 'maturing_debt', 'gfn']]
gfn_emde['country'] = gfn_emde['ifscode'].map(ifs_to_countryname)
gfn_emde = gfn_emde.sort_values('country')

gfn = pd.concat([gfn_ae, gfn_emde]).sort_values('country')

# Gross financing needs: EMDE - alternative source: EDI
# vintage = '2023-04'
# edi_amo = edi_utilities.get_edi_csd_ccx_data('all', 'G_AMO', freq='A', vintage='2023-04', exercise='VEE', longformat=True).rename(columns={'country': 'ifscode'})
# edi_amo['year'] = edi_amo['dates'].dt.year
# edi_amo['ifscode'] = edi_amo['ifscode'].astype('int')
# check = gfn.merge(edi_amo, on=['ifscode', 'year'], how='left')
# check_em = check.inlist('ifscode', dum.emde)