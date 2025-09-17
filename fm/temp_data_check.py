import imf_datatools
from fadfpdata import cname_to_ifs

varlist = ['GGR_GDP', 'GGX_GDP']
weo = imf_datatools.get_ecos_sdmx_data('WEO_WEO_LIVE', 'all', varlist, longformat=True)

check = weo[weo['COUNTRY']=='147']