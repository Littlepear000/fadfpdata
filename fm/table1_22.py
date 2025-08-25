import imf_datatools
import pandas as pd
import pandaspro as cpd
from fadfpdata import cname_to_ifs

# varlist = [
#     'GGXCNL_NGDP',
#     'GGXONLB_NGDP',
#     'GGCAB_NPGDP_N',
#     'GGCABP_NPGDP_N',
#     'GGR_NGDP',
#     'GGX_NGDP',
#     'GGXWDG_NGDP',
#     'GGXWDN_NGDP'
# ]
# fm = imf_datatools.get_ecos_sdmx_data('WEO_FM_LIVE_3', 'all', varlist, longformat=True)

fm['ifscode'] = pd.to_numeric(fm['COUNTRY'], errors='coerce')
fm = fm.dropna(subset=['ifscode'])
fm['ifscode'] = fm['ifscode'].astype('int')

template = cpd.pwread(r'fm/template/Stat_Tables1-22.xlsx', sheet_name='STAT1', cellrange='C:C')[0]
template.columns=['country']
template = template.dropna()
template['ifscode'] = template['country'].map(cname_to_ifs)
