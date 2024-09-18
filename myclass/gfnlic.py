from fadfpdata.myclass.ImfFrame import ImfFrame
from pandaspro import cpdBaseFrame
from fadfpdata import database_root

gfnlic_im_rename = {
    'ifs_code': 'ifscode',
    'horizon_year': 'year',
    'first_year_of_projection': 'vintage_year',
    'dugfn_gdp': 'gfn'
}

@cpdBaseFrame(
    path=fr'{database_root}\GFN\lic',
    file_type='xlsx',
    sheet_name='data',
    imr=gfnlic_im_rename,
    dvl=['ifscode', 'year', 'gfn']
)
class GfnLic(ImfFrame):
    def __getattr__(self, item):
        if item.startswith('vinl'):
            onlykeepyear = int(item[4:])
            return self.groupby('ifscode').apply(lambda x: x[
                (x['vintage_year'] == max(x['vintage_year'])) &
                (x['issue_date'] == max(x['issue_date'])) &
                (x['year'] == onlykeepyear)
            ])
        else:
            return super().__getattr__(item)


if __name__ == '__main__':
    d = GfnLic()
