from pandaspro import FramePro
from pandaspro.cpdbase.cpd_base_frame import cpdBaseFrame

cg_path = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Databases\CountryGrouping'


@cpdBaseFrame(path=cg_path, file_type='xlsx')
class CountryGrouping(FramePro):

    def get_by_groupcode(self, code):
        clist = self.inlist('group_code', code)['country_code'].dropna().tolist()
        return [int(c) for c in clist]


if __name__ == '__main__':
    a = CountryGrouping()
    # b = a.df[['ifscode', 'emde']]

