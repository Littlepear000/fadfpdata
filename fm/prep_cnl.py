import sprnldata as spr
from sprnldata.myclass.dummy import Dummy

curr_year = 2024
ecos = spr.ecos()
dum = Dummy()

raw = ecos.br('ifscode; year; ggxcnl_gdp')[(ecos['year'] >= curr_year) & (ecos['year'] <= curr_year+5)]
cnl = raw.pivot_table(index='ifscode',
                      values='ggxcnl_gdp',
                      aggfunc='mean').reset_index()