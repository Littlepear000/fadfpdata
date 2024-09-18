import pandas as pd
from fadfpdata.myclass.ImfFrame import ImfFrame
from fadfpdata.downloads.weovintage import folder_vintage
from fadfpdata.utils.core import get_latest_file


class WeoVinage(ImfFrame):
    def __init__(self,
                 *args,
                 version='latest',
                 **kwargs
                 ):
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            local_version = get_latest_file(folder_vintage) if version == 'latest' else version
            raw = pd.read_csv(f'{folder_vintage}/WEOvintages_{local_version}.csv')
            super().__init__(raw)

        self.idvar = ['ifscode', 'vintage_year', 'year']

    @property
    def _constructor(self):
        return WeoVinage

    def keep_var(self, varlist: str):
        keeplist = '; '.join(self.idvar) + '; ' + varlist
        return self.br(keeplist)


if __name__ == '__main__':
    a = WeoVinage(version='latest')
    b = a.y2005

    # years = (2006, 2008)
    # c = a.keep_var('ngdp; iar_bp6')
