from fadfpdata.mydata.ImfFrame_fadfp import ImfFrame_FADFP
# noinspection PyUnresolvedReferences
from pandaspro import cpdBaseFrame

ecos_im_rename = {

}

@cpdBaseFrame(
    path=r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Databases\ECOS\Ecos',
    file_type='csv',
    prefix='ecosdata',
    imr=ecos_im_rename,
    dvl=['ifscode', 'year']
)
class ecos(ImfFrame_FADFP):
    def __getattr__(self, item):
        my_varlists = item.split('_')
        valid_varlists = [var for var in my_varlists if var in self.columns]
        if len(valid_varlists) != 0 and len(valid_varlists) == len(my_varlists):
            return self.dvlmore(valid_varlists)
        else:
            return super().__getattr__(item)


if __name__ == '__main__':
    d = ecos()
