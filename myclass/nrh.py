from fadfpdata.myclass.ImfFrame import ImfFrame
# noinspection PyUnresolvedReferences
from pandaspro import cpdBaseFrame
from fadfpdata import database_root

nrh_im_rename = {

}

@cpdBaseFrame(
    path=fr'{database_root}\NRH',
    file_type='csv',
    prefix='nrh',
    imr=nrh_im_rename,
    default_version='latest'
)
class Nrh(ImfFrame):
    def __getattr__(self, item):
        my_varlists = item.split('_')
        valid_varlists = [var for var in my_varlists if var in self.columns]
        if len(valid_varlists) != 0 and len(valid_varlists) == len(my_varlists):
            return self.dvlmore(valid_varlists)
        else:
            return super().__getattr__(item)


if __name__ == '__main__':
    d = Nrh()
