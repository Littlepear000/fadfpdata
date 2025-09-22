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
        weo_update_date,
        blmbg_update_date,
        wbnrh_update_date,
        ep_update_date,
        ep_start_year: int =2024
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
        final_table = pd.concat([agg_all, table.drop('ifscode', axis=1)])
        final_table = final_table.reset_index().drop('index', axis=1).fillna('...')
        final_table.loc[final_table['country'].isin(self.group_dict.k]

if __name__ == '__main__':
    pass