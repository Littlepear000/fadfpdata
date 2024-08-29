from fadfpdata.fm import *

raw = ecos.br('ifscode; year; ggxcnl_gdp')[(ecos['year'] >= curr_year) & (ecos['year'] <= curr_year+5)]
cnl = raw.pivot_table(index='ifscode',
                      values='ggxcnl_gdp',
                      aggfunc='mean').reset_index()