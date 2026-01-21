from fadfpdata.fm import *

data = weodata[['ifscode', 'year', 'ggei', 'ggxwdg', 'ngdp', 'ggxcnl_gdp']].query('year >= 2000')
data['g'] = data.groupby('ifscode')['ngdp'].pct_change()
data['ggxwdg_l'] = data.groupby('ifscode')['ggxwdg'].shift(1)
data['r'] = np.where(data['ggxwdg_l'] == 0, np.nan, data['ggei'] / data['ggxwdg_l'])
data['rlessg'] = np.where((1 + data['g']) == 0, np.nan,
                          (data['r'] - data['g'])/(1 + data['g']) * 100)



rlessg = data[(data['year']>=curr_year) & (data['year']<=curr_year+5)]
rlessg = rlessg.groupby('ifscode')['rlessg'].mean().reset_index()

# Countries to be excluded
hide_list = ['Venezuela']
for country in hide_list:
    rlessg.loc[rlessg['ifscode'] == cname_to_ifs[country], 'rlessg'] = np.nan
