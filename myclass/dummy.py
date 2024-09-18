import pandas as pd
import numpy as np
from pandaspro import FramePro
from pandaspro.cpdbase.cpd_base_frame import cpdBaseFrame


dummy_path = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Databases\Dummy'


@cpdBaseFrame(path=dummy_path, file_type='xlsx')
class Dummy(FramePro):

    def __getattr__(self, item):
        if item in self.columns:
            return self.inlist(item, 1)['ifscode'].tolist()
        else:
            return super().__getattr__(item)

    @property
    def g20(self):
        return self.inlist('g20_adv', 1)['ifscode'].tolist() + self.inlist('g20_em', 1)['ifscode'].tolist()

    @property
    def ae_noUS(self):
        return [c for c in self.inlist('ae', 1)['ifscode'].tolist() if c != 111]

    @property
    def em_noChina(self):
        return [c for c in self.inlist('em', 1)['ifscode'].tolist() if c != 924]

if __name__ == '__main__':
    from fadfpdata.myclass.country_grouping import CountryGrouping as cg
    a = Dummy()
    b = cg().get_by_groupcode(200)
    c = a.inlist('ifscode', b, engine='c', rename='emde').df
    # b = a.df[['ifscode', 'emde']]

