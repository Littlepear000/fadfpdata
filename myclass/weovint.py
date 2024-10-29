from fadfpdata.myclass.ImfFrame import ImfFrame
# noinspection PyUnresolvedReferences
from pandaspro import cpdBaseFrame
from fadfpdata import database_root
import pandas as pd

weovint_im_rename = {

}

@cpdBaseFrame(
    path=fr'{database_root}\ECOS\WEOvint',
    file_type='csv',
    prefix='WEOvint',
    dateid = '%Y%m',
    imr=weovint_im_rename,
    default_version='latest'
)
class WeoVint(ImfFrame):
    pass



if __name__ == '__main__':
    d = WeoVint(version='202407')
