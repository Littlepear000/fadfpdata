from fadfpdata.myclass.ImfFrame import ImfFrame
# noinspection PyUnresolvedReferences
from pandaspro import cpdBaseFrame
from fadfpdata import database_root
import pandas as pd

weovint_im_rename = {

}

def weovint_load(df):
    df['ggr_d'] = df['ggr'] / df['enda']
    df['ggei_d'] = df['ggei'] / df['enda']
    df['ggei_ggr'] = df['ggei'] / df['ggr'] * 100
    df['ggei_ggr_net'] = (df['ggei'] - df['ggropi']) / df['ggr'] * 100
    return df

@cpdBaseFrame(
    path=fr'{database_root}\ECOS\WEOvint',
    file_type='csv',
    prefix='WEOvint',
    dateid = '%Y%m',
    imr=weovint_im_rename,
    default_version='latest',
    load=weovint_load
)
class WeoVint(ImfFrame):
    pass



if __name__ == '__main__':
    d = WeoVint(version='202407')
