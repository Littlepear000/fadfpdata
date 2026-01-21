from fadfpdata.fm import *

raw = weodata.br('ifscode; year; ggxcnl_gdp')[(weodata['year'] >= curr_year) & (weodata['year'] <= curr_year + 5)]
cnl = raw.pivot_table(index='ifscode',
                      values='ggxcnl_gdp',
                      aggfunc='mean').reset_index()