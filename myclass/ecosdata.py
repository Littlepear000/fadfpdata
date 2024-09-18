import pandas as pd
import re
from fadfpdata.myclass.ImfFrame import ImfFrame
from fadfpdata.downloads.ecos.ecosset import folder_ecos
from fadfpdata.utils.core import get_latest_file


class EcosData(ImfFrame):
    def __init__(self,
                 *args,
                 version='latest',
                 **kwargs
                 ):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            local_version = get_latest_file(folder_ecos) if version == 'latest' else version
            raw = pd.read_csv(f'{folder_ecos}/ecosdata_{local_version}.csv')
            super().__init__(raw)

        self.idvar = ['ifscode', 'year']

    def __getattr__(self, item):
        if re.fullmatch(r'y\d{4}', item):
            keepkey = int(re.fullmatch(r'y(\d{4})', item).group(1))
            return self.inlist('year', keepkey)
        elif re.fullmatch(r'y\d{4}_\d{4}', item):
            startyear = int(re.fullmatch(r'y(\d{4})_(\d{4})', item).group(1))
            endyear = int(re.fullmatch(r'y(\d{4})_(\d{4})', item).group(2))
            return self.inlist('year', [i for i in range(startyear, endyear+1)])
        elif re.fullmatch(r'y(\d+)', item):
            numbers = re.fullmatch(r'y(\d+)', item).group(1)
            if len(numbers) % 4 == 0:
                years = [int(numbers[i: i+4]) for i in range(0, len(numbers), 4)]
                return self.inlist('year', years)
            else:
                raise ValueError('Enter separate years in 4-digit format, eg. 200120042008 for year 2001, 2004 and 2008')
        else:
            return super().__getattr__(item)


    @property
    def _constructor(self):
        return EcosData

    @property
    def wdi(self):
        wdivars = [i for i in self.columns if '.' in i]
        return self[['ifscode', 'year'] + wdivars]

    def keep_var(self, varlist: str):
        keeplist = '; '.join(self.idvar) + '; ' + varlist
        return self.br(keeplist)


if __name__ == '__main__':
    from fadfpdata.utils.core import ifs_to_countryname

    a = EcosData(version='latest')
    # b = a.dummy
    # c = b.expand_column(['repeat_ufr', 'emde']).dropna(subset=['expand_value']).rename(
    #         columns={'expand_value': 'group'})
    # d = c.df
    e = a.create_boxplot_data(group_dummies=['repeat_ufr', 'emde'],
                              varname='si.pov.gini',
                              year='latest',
                              keep_group=['Challenging Repeat Users', 'Regular Repeat Users', 'FCLs/PLLs', 'EMDE'])
    f = e.df