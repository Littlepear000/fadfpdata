import pandas as pd
import pandaspro as cpd
import re
from pandaspro import CellPro
from pandaspro.core.frame import FramePro
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.utils.core import weighted_avg, ifs_to_countryname, inc_dict


def filter_year(df, years: str, ftype: str):
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

def gen_forecast_error(
        df,
        vintage_data,
        indicator: str | list,
        vintage_year: str ='T-1',
        vintage_month: str = 'Oct'
):

    if isinstance(indicator, str):
        ind_list = [indicator]
    else:
        ind_list = indicator

    if vintage_year == 'T':
        adj = 0
    elif vintage_year.startswith('T'):
        adj = int(vintage_year.replace('T', ''))
    else:
        raise ValueError('vintage_year must start with T (eg. T, T-1, T-2)')

    ecos_long = df.melt(id_vars=['ifscode', 'year'],
                          value_vars=ind_list,
                          var_name='indicator',
                          value_name='actual')
    ecos_long['vintage_year'] = ecos_long['year'] + adj

    weovint_select = vintage_data[vintage_data['vintage_year'].str.contains(vintage_month)]
    weovint_select['vintage_year'] = weovint_select['vintage_year'].str.replace(vintage_month, '').astype('int')
    weovint_long = weovint_select.melt(id_vars=['ifscode', 'vintage_year', 'year'],
                                       value_vars=ind_list,
                                       var_name='indicator',
                                       value_name='forecast')

    combine = weovint_long.merge(ecos_long,
                                 on=['ifscode', 'indicator', 'vintage_year', 'year'],
                                 how='left')
    combine['forecast_error'] = combine['forecast'] - combine['actual']
    final = combine[combine['vintage_year'] == combine['year'] + adj]
    return final

class ImfFrame(FramePro):
    def __getattr__(self, item):
        if (re.fullmatch(r'[yvse]\d{4}', item) or
                re.fullmatch(r'[yvse]\d{4}_\d{4}', item) or
                re.fullmatch(r'[yvse]\d+', item)):
            ftype = item[0]
            years = item[1:]
            return filter_year(self, years=years, ftype=ftype)
        elif item.startswith('vinl'):
            onlykeepyear = int(item[4:])
            return self.groupby('ifscode').apply(
                lambda x: x[(x['vintage_year'] == max(x['vintage_year'])) & (x['year'] == onlykeepyear)])
        # Inlist with Dummies
        elif item in ['keep2018', 'keep2025']:
            return self.inlist(item.replace('keep', 'roc'), 1)
        elif item in self.columns and item not in self.idvar:
            return self[self.idvar + [item]]
        else:
            return super().__getattr__(item)

    @property
    def dummy(self):
        countrydummy = Dummy()
        return pd.merge(self, countrydummy, on='ifscode', how='left')

    @property
    def add_cname(self):
        newdf = self.copy()
        newdf['country'] = newdf['ifscode'].map(ifs_to_countryname)
        return newdf.corder('country')

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

    def agg_mean(self, indicator, group_dict=inc_dict, weight='ngdpd'):
        df_append = pd.DataFrame()
        if weight:
            for group, gr_list in group_dict.items():
                filtered_df = self.inlist('ifscode', gr_list)
                df_mean = filtered_df.groupby('year').apply(
                    lambda x: weighted_avg(x, indicator, weight=weight)).reset_index().rename(
                    columns={0: indicator})
                df_mean['group'] = group
                df_append = pd.concat([df_append, df_mean])
        else:
            for group, gr_list in group_dict.items():
                filtered_df = self.inlist('ifscode', gr_list)
                df_mean = filtered_df.groupby('year')[indicator].mean().reset_index().rename(columns={0: indicator})
                df_mean['group'] = group
                df_append = pd.concat([df_append, df_mean])
        df_wide = df_append.pivot(index='year', columns='group', values=indicator)
        df_wide = FramePro(df_wide).corder(list(group_dict.keys()))
        return df_wide

    def agg_median(self, indicator, group_dict):
        df_append = pd.DataFrame()
        for group, gr_list in group_dict.items():
            filtered_df = self.inlist('ifscode', gr_list)
            df_mean = filtered_df.groupby('year').agg({indicator: 'median'}).reset_index()
            df_mean['group'] = group
            df_append = pd.concat([df_append, df_mean])
        df_wide = df_append.pivot(index='year', columns='group', values=indicator)
        df_wide = FramePro(df_wide).corder(list(group_dict.keys()))
        return df_wide

    def export_agg_detail(
            self,
            indicator: str,
            excel_file: str,
            sheet_name: str,
            group_dict: dict = inc_dict,
            weight: str = 'ngdpd',
            start_cell: str = 'A1',
            direction: str = 'right',
    ):
        output = pd.DataFrame()
        ps = cpd.PutxlSet(excel_file)
        ps.tab(sheet_name)

        for group, list in group_dict.items():

            filtered_df = self[self['ifscode'].isin(list)]
            result = filtered_df.groupby('year').agg(
                mean=(indicator, 'mean'),
                weighted_avg=(indicator, lambda x: weighted_avg(filtered_df.loc[x.index], indicator, weight=weight)),
                median=(indicator, 'median'),
                p25=(indicator, lambda x: x.quantile(0.25)),
                p75=(indicator, lambda x: x.quantile(0.75)),
                p10=(indicator, lambda x: x.quantile(0.1)),
                p90=(indicator, lambda x: x.quantile(0.9)),
            ).reset_index()
            result['interquartile'] = result['p75'] - result['p25']
            result['10-90th'] = result['p90'] - result['p10']

            result_copy = cpd.FramePro(result.copy())
            result_copy['group'] = group
            result_copy = result_copy.corder('group')
            output = pd.concat([output, result_copy])

            ps.putxl(group, cell=CellPro(start_cell).offset(-1, 0).cell)
            ps.putxl(result, cell=start_cell, index=False)
            if direction == 'right':
                start_cell = CellPro(ps.next_cell_right.cell).offset(0, 2).cell
            elif direction == 'down':
                start_cell = CellPro(ps.next_cell_down.cell).offset(3, 0).cell

    def gen_forecast_error_long(
            self,
            vintage_data: pd.DataFrame,
            indicator: str | list,
            vintage_year: str ='T-1',
            vintage_month: str = 'Oct'
    ):
        return gen_forecast_error(self, vintage_data=vintage_data, indicator=indicator, vintage_year=vintage_year, vintage_month=vintage_month)

    def gen_forecast_error_wide(
            self,
            vintage_data: pd.DataFrame,
            indicator: str | list,
            vintage_year: str ='T-1',
            vintage_month: str = 'Oct'
    ):
        forecast_error_long = gen_forecast_error(self, vintage_data=vintage_data, indicator=indicator, vintage_year=vintage_year, vintage_month=vintage_month)
        forecast_error_wide = forecast_error_long.pivot_table(index=['ifscode', 'year'], columns='indicator', values='forecast_error').reset_index()
        return forecast_error_wide


if __name__ == '__main__':
    a = FramePro().expand_column
