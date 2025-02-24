from pandaspro import FramePro
from pandaspro.cpdbase.cpd_base_frame import cpdBaseFrame
from fadfpdata import database_root


@cpdBaseFrame(path=fr'{database_root}\Dummy', file_type='xlsx')
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
    def eur(self):
        return self.inlist('adv_eur', 1)['ifscode'].tolist() + self.inlist('em_eur', 1)['ifscode'].tolist()

    @property
    def ae_noUS(self):
        return [c for c in self.inlist('ae', 1)['ifscode'].tolist() if c != 111]

    @property
    def em_noChina(self):
        return [c for c in self.inlist('em', 1)['ifscode'].tolist() if c != 924]

if __name__ == '__main__':
    from fadfpdata.myclass.country_grouping import CountryGrouping as cg
    a = Dummy()


