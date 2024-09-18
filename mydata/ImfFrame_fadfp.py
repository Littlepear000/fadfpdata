import pandas as pd
import re
from pandaspro.core.frame import FramePro
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.utils.core import ifs_to_countryname


class ImfFrame_FADFP(FramePro):
    def __getattr__(self, item):
        def _filter_year(df, years: str, ftype: str):
            ftype_dict = {
                'y': 'year',
                'v': 'vintage_year',
                's': 'app_year',
                'e': 'end_year'
            }
            if re.fullmatch(r'\d{4}', years):
                keepkey = int(re.fullmatch(r'(\d{4})', years).group(1))
                print(ftype_dict[ftype], keepkey)
                return df.inlist(ftype_dict[ftype], keepkey)
            elif re.fullmatch(r'\d{4}_\d{4}', years):
                startyear = int(re.fullmatch(r'(\d{4})_(\d{4})', years).group(1))
                endyear = int(re.fullmatch(r'(\d{4})_(\d{4})', years).group(2))
                return df.inlist(ftype_dict[ftype], [i for i in range(startyear, endyear + 1)])
            elif re.fullmatch(r'(\d+)', years):
                numbers = re.fullmatch(r'(\d+)', years).group(1)
                if len(numbers) % 4 == 0:
                    return df.inlist(ftype_dict[ftype], years)
                else:
                    raise ValueError(
                        'Enter separate years in 4-digit format, eg. 200120042008 for year 2001, 2004 and 2008')
            else:
                raise ValueError('Invalid years input in para')

        # Years Play
        if (re.fullmatch(r'[yvse]\d{4}', item) or
                re.fullmatch(r'[yvse]\d{4}_\d{4}', item) or
                re.fullmatch(r'[yvse]\d+', item)):
            ftype = item[0]
            years = item[1:]
            return _filter_year(self, years=years, ftype=ftype)
        # Inlist with Dummies
        # elif item in ['keep2018', 'keep2025']:
        #     return self.inlist(item.replace('keep', 'roc'), 1)

        # Vintage Latest
        elif item.startswith('vinl'):
            onlykeepyear = int(item[4:])
            return self.groupby('ifscode').apply(lambda x: x[(x['vintage_year'] == max(x['vintage_year'])) & (x['year'] == onlykeepyear)])

        else:
            return super().__getattr__(item)

    @property
    def dummy(self):
        countrydummy = Dummy()
        return pd.merge(self, countrydummy, on='ifscode', how='left')

    def get_latest_available_data(self, varname: str):
        filtered_df = self.dropna(subset=[varname])
        latest_df = filtered_df.sort_values('year').groupby('ifscode').tail(1)
        result_df = latest_df[['ifscode', 'year', varname]].rename(columns={'year': 'latest_available_year'})
        return result_df

    def create_boxplot_data(self,
                            group_dummies: list,
                            varname: str | list,
                            year: int | str,
                            keep_group: list = None):
        varlist = [varname] if isinstance(varname, str) else varname

        if isinstance(year, int):
            final_cols = ['group', 'country', 'ifscode', 'year'] + varlist
            df = self[self['year'] == year]
        if isinstance(year, str):
            final_cols = ['group', 'country', 'ifscode', 'latest_available_year'] + varlist
            df = self.get_latest_available_data(varname)

        df = df.dummy.expand_column(group_dummies).dropna(subset=['expand_value']).rename(
                columns={'expand_value': 'group'})[final_cols].sort_values('group')
        if keep_group:
            df = df[df['group'].isin(keep_group)]
            df['group'] = pd.Categorical(df['group'], categories=keep_group, ordered=True)
            df = df.sort_values('group').reset_index(drop=True)
        return df

    def create_individual_col_data(self):
        pass

if __name__ == '__main__':
    a = FramePro().expand_column
