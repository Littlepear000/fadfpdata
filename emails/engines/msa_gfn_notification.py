import pandas as pd
import pandaspro as cpd
from fadfpdata.fm.prep_gfn import gfn

desk_info = cpd.pwread(r'Q:\DATA\FP\Fiscal Monitor\2024-10-October_Monitor\MSA\input sources\country desk info.xlsx', sheet_name='info')[0]
desk_info['email_list'] = desk_info.apply(lambda row: '; '.join(filter(pd.notna, [row['email1'], row['email2'], row['email3'], row['email4']])), axis=1)
combined_info = desk_info.merge(gfn, on='ifscode', how='left')

# noinspection PyTypedDict
class msa_gfn_notification(cpd.emailfetcher):
    # noinspection PyAttributeOutsideInit
    def fetch_data(self, ifscode=None, year=2024):
        self.input = {}
        self.data_pick = {}
        for col in ['country', 'gfn', 'deficit', 'maturing_debt', 'email_list']:
            self.data_pick[col] = combined_info.set_index('ifscode').at[ifscode, col]

        self.input['__[COUNTRY]__'] = self.data_pick['country']
        self.input['__[GFN_TOTAL]__'] = round(self.data_pick['gfn'], 1)
        self.input['__[DEFICIT]__'] = round(self.data_pick['deficit'], 1)
        self.input['__[AMORT]__'] = round(self.data_pick['maturing_debt'], 1)
        if pd.isna(self.data_pick['maturing_debt']):
            self.input['__[NOTE]__'] = f"In the case of {self.data_pick['country']}, the overall government deficit for {year} is {round(self.data_pick['deficit'], 1)}%, but the GGDS data is not available in WEO. Therefore, the GFN will be shown as missing. If you would like to show the GFN for {self.data_pick['country']}, please kindly provide the government debt amortization in percent of GDP for {year}. And we can calculate the GFN accordingly. Thank you very much!"
        else:
            self.input['__[NOTE]__'] = f"In the case of {self.data_pick['country']}, we have now calculated the GFN for {year} as {round(self.data_pick['gfn'], 1)}%, with overall government deficit being {round(self.data_pick['deficit'], 1)}% and debt amortization being {round(self.data_pick['maturing_debt'], 1)}%. Please let us know if the numbers are ok from your side. Thank you very much!"

        # Subject, To and CC
        self.input['__subject__'] = 'For the October Fiscal Monitor Appendix: Change in methodology of Gross Financing Needs calculation'
        self.input['__to__'] = self.data_pick['email_list']
        self.input['__cc__'] = "ASolovyeva@imf.org"

        return self.input

    # noinspection PyAttributeOutsideInit
    def fetch_showitems(self, **kwargs):
        self.render_dict = {}
        if pd.isna(self.data_pick['maturing_debt']):
            self.render_dict['show_1'] = True
            self.render_dict['show_2'] = False
        else:
            self.render_dict['show_1'] = False
            self.render_dict['show_2'] = True
        return self.render_dict
