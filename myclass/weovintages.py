import pandas as pd
from fadfpdata.myclass.ImfFrame import ImfFrame
from fadfpdata.downloads.weovintages import folder_vintage
from fadfpdata.utils.core import get_latest_file


class WeoVinages(ImfFrame):
    def __init__(self,
                 *args,
                 month='Apr',
                 version='latest',
                 **kwargs
                 ):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            local_version = get_latest_file(f'{folder_vintage}/{month}') if version == 'latest' else version
            raw = pd.read_csv(f'{folder_vintage}/{month}/WEOvintages_{month}_{local_version}.csv')
            super().__init__(raw)

    @property
    def _constructor(self):
        return WeoVinages

    def keep_var(self, varlist: str):
        keeplist = '; '.join(['ifscode', 'vintage_year', 'year']) + '; ' + varlist
        return self.br(keeplist)


if __name__ == '__main__':
    a = WeoVinages(version='latest')
    b = a.y2005

    # years = (2006, 2008)
    # c = a.keep_var('ngdp; iar_bp6')
