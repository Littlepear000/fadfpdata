from fadfpdata.myclass.weovintages import WeoVinages
from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.myclass.weovint import WeoVint


weovint = WeoVinages()
ecos = EcosData()
# ind_list = [col for col in ecos.columns if col not in ['ifscode', 'year', 'dates']]
ind_list = ['ggxonlb_gdp', 'ggr_gdp', 'ggx_gdp', 'ggxwdg_gdp']
vint_month = 'Oct'

test_wide = ecos.gen_forecast_error_wide(vintage_data= weovint, indicator=ind_list, vintage_year='T-1', vintage_month=vint_month)
test_agg = test_wide.agg_mean(indicator='ggxwdg_gdp', weight=None)

test_long = ecos.gen_forecast_error_long(vintage_data= weovint, indicator=ind_list, vintage_year='T-1', vintage_month=vint_month)
test_long[test_long['ifscode'] == 111].to_excel('temp.xlsx')

weo202410 = WeoVint(version='201010')
check_vint = weo202410[['ifscode', 'year', 'ggxwdg_gdp']].inlist('ifscode', 111).query('year>=2000')

# # forecast for year T based on T-1 Oct WEO vintage
# ecos_long = ecos.melt(id_vars=['ifscode', 'year'],
#                       value_vars=ind_list,
#                       var_name='indicator',
#                       value_name='actual')
# ecos_long['vintage_year'] = ecos_long['year'] - 1
#
# weovint_select = weovint[weovint['vintage_year'].str.contains(vint_month)]
# weovint_select['vintage_year'] = weovint_select['vintage_year'].str.replace(vint_month, '').astype('int')
# weovint_long = weovint_select.melt(id_vars=['ifscode', 'vintage_year', 'year'],
#                       value_vars=ind_list,
#                       var_name='indicator',
#                       value_name='forecast')
#
# combine = weovint_long.merge(ecos_long,
#                              on=['ifscode', 'indicator', 'vintage_year', 'year'],
#                              how='left')
# combine['forecast_error'] = combine['forecast'] - combine['actual']
# final = combine[combine['vintage_year'] == combine['year']-1]
# final[final['ifscode'] == 111].to_excel('temp.xlsx')

