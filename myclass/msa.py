import pandas as pd
import pandaspro as cpd
from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.fm.prep_ep import ep
from fadfpdata.fm.prep_cnl import cnl
from fadfpdata.fm.prep_gfn import gfn
from fadfpdata.fm.prep_rlessg import rlessg
from fadfpdata.fm.prep_to_maturity import d_to_m
from fadfpdata.fm.prep_non_resholding import nrh

ecos = EcosData()
dum = Dummy()

class msa:
    def __init__(
        self,
        curr_year,
        input_folder,
        output_folder,
        # 原本放在 __init__.py 的参数
        fm_version,
        fm_folder_name,
        blmbg_update_date,
        wbnrh_update_date,
        weo_update_date,
        ep_update_date,
        ep_start_year
    ):
        # 基本参数
        self.curr_year = curr_year
        self.input_folder = input_folder
        self.output_folder = output_folder

        # fm init.py 里的参数
        self.fm_version = fm_version
        self.fm_folder_name = fm_folder_name
        self.blmbg_update_date = blmbg_update_date
        self.wbnrh_update_date = wbnrh_update_date
        self.weo_update_date = weo_update_date
        self.ep_update_date = ep_update_date
        self.ep_start_year = ep_start_year

        # 动态生成 col_ren
        self.col_ren = {
            'country': '',
            f'Y_{self.ep_start_year}_to_2030_pension': f'Pension Spending Change, {self.ep_start_year}–30',
            f'NPV{self.ep_start_year}_2050_pension': f'Net Present Value of Pension Spending Change, {self.ep_start_year}–50',
            f'Y_{self.ep_start_year}_to_2030_health': f'Health Care Spending Change, {self.ep_start_year}–30',
            f'NPV{self.ep_start_year}_2050_health': f'Net Present Value of Health Care Spending Change, {self.ep_start_year}–50',
            'gfn': 'Gross Financing Need, 2024',
            'years_to_maturity': 'Average Term to Maturity, 2024 (years)',
            'debt_to_maturity': 'Debt to Average Maturity, 2024',
            'rlessg': 'Projected Interest Rate–Growth Differential, 2024–29 (percent)',
            'pre_pan_cnl': 'Pre-Pandemic Overall Balance, 2012–19',
            'ggxcnl_gdp': 'Projected Overall Balance, 2024–29',
            'nrh': 'Nonresident Holding of General Government Debt, 2023 (percent of total)',
            'nfw': 'Net Financial Worth of General Government, 2021 (percent of GDP)'
        }

        # 各类分组与数值
        self.group_dict = {
            'AE': dum.ae,
            'EM': dum.em,
            'LIC': dum.lic,
            'G7': dum.g7,
            'G20': dum.g20,
            'G20_adv': dum.g20_adv,
            'G20_em': dum.g20_em
        }
        self.pre_pan_cnl_dict = {
            'AE': -3.1,
            'EM': -3.1,
            'LIC': -3.3,
            'G7': -4.0,
            'G20_adv': -3.6,
            'G20_em': -3.5
        }
        self.stat23_25_dict = {
            'STAT23': 'B3:B42',
            'STAT24': 'B3:B47',
            'STAT25': 'B3:B43',
        }

    def weighted_avg(self, group, indicator):
        group = group.dropna(subset=[indicator, 'ngdp_fy_usd'])
        return (group[indicator] * group['ngdp_fy_usd']).sum() / group['ngdp_fy_usd'].sum()

    def prepare_table(self):
        ngdpd_fy = ecos.query(f'year == {self.curr_year}')[['ifscode', 'ngdp_fy_usd']]
        fix_col = pd.read_excel(fr'{self.input_folder}\fixed columns.xlsx', sheet_name='combine')
        table = fix_col.copy()
        for df in [ep, cnl, gfn, rlessg, d_to_m, nrh, ngdpd_fy]:
            table = table.merge(df, on='ifscode', how='left')
        return cpd.FramePro(table)

    def aggregate_groups(self, table):
        agg_all = pd.DataFrame()
        for group in self.group_dict.keys():
            df_group = table.inlist('ifscode', self.group_dict[group])
            weighted_avg = {}
            for col in [col for col in df_group.columns if col not in ['country', 'ifscode', 'ngdpd_fy']]:
                weighted_avg[col] = (df_group[col] * df_group['ngdp_fy_usd']).sum() / df_group['ngdp_fy_usd'].sum()
            agg = pd.DataFrame(weighted_avg, index=[group])
            agg_all = pd.concat([agg_all, agg])
        return agg_all.reset_index().rename(columns={'index': 'country'})

    def finalize_table(self, agg_all, table):
        final_table = pd.concat([agg_all, table.drop('ifscode', axis=1)])[self.col_ren.keys()]
        final_table = final_table.reset_index().drop('index', axis=1).fillna('...')
        final_table.loc[final_table['country'].isin(self.group_dict.keys()), 'nfw'] = ''
        final_table.loc[final_table['country'].isin(self.pre_pan_cnl_dict.keys()), 'pre_pan_cnl'] = \
            final_table['country'].map(self.pre_pan_cnl_dict)
        return final_table

    def export_to_excel(self, final_table):
        output_file = fr'{self.output_folder}\Stat_Tables23-25_FM{self.fm_folder_name}_{self.weo_update_date}.xlsx'
        ps = cpd.PutxlSet(output_file)
        for sheet, cellrange in self.stat23_25_dict.items():
            country_order = cpd.pwread(output_file, sheet_name=sheet, cellrange=cellrange)[0].rename(
                columns={'unnamed_1': 'country'})
            table_final = country_order.merge(final_table, on='country', how='left')
            ps.putxl(table_final.drop('country', axis=1), sheet_name=sheet, cell='C4', header=False, index=False)

    def run(self):
        table = self.prepare_table()
        agg_all = self.aggregate_groups(table)
        final_table = self.finalize_table(agg_all, table)
        self.export_to_excel(final_table)
