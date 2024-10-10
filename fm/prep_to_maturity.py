from fadfpdata.fm import *

# Average term to maturity - source: Bloomberg
maturity_raw = cpd.pwread(fr'{input_folder}/Bloomberg_Years_to_Maturity.xlsx', sheet_name=blmbg_update_date, cellrange='H:I')[0].drop(0)
maturity_raw.columns = ['country', 'years_to_maturity']
maturity_raw['ifscode'] = maturity_raw['country'].map(cname_to_ifs)
maturity = maturity_raw.dropna(subset='ifscode')[['ifscode', 'years_to_maturity']]

# Countries to be excluded
hide_list = ['Hong Kong', 'Lebanon', 'Sri Lanka']
for country in hide_list:
    maturity.loc[maturity['ifscode'] == cname_to_ifs[country], 'years_to_maturity'] = np.nan

# maturity.loc[maturity['ifscode'] == 532, 'years_to_maturity'] = np.nan  # change Hong Kong to missing
# maturity.loc[maturity['ifscode'] == 446, 'years_to_maturity'] = np.nan  # change Lebanon to missing

# Debt to average maturity - source: Bloomberg + WEO
weo_debt = ecos[['ifscode', 'year', 'ggxwdg_gdp']].inlist('year', curr_year)
d_to_m = maturity.merge(weo_debt, on='ifscode', how='left').drop('year', axis=1)
d_to_m['debt_to_maturity'] = d_to_m['ggxwdg_gdp'] / d_to_m['years_to_maturity']
