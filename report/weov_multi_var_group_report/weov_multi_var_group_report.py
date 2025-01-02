from report.report import report
import pandaspro as cpd
from fadfpdata.myclass.weovint import WeoVint


class WeovMultiVarGroupReport(report):
    rpath = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_My Projects\Weov Multi Var Group Report'

    def __init__(
            self,
            varlist,
            vintages,
            *args,
            startyear = 2000,
            weight = 'ggr_d',
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.varlist = varlist
        self.startyear = startyear
        self.vintages = vintages
        self.weight = weight

    def gen(
            self,
            ps=None,
            filename: str = None,
            exclude: list = None
    ):
        if ps is None:
            if filename is None:
                filename = f'temp.xlsx'
            ps = cpd.PutxlSet(WeovMultiVarGroupReport.rpath + '/' + filename)
        else:
            ps = ps

        ps.tab('instruction')
        ps.putxl(', '.join(self.varlist), cell='A1')
        ps.putxl(', '.join(self.vintages), cell='A2')
        ps.putxl(f'weight = {self.weight}', cell='A3')
        ps.putxl(f'startyear = {self.startyear}', cell='A4')

        for var in self.varlist:
            for vin in self.vintages:
                df = WeoVint(version=vin).query(f'year >= {self.startyear}')
                df.export_agg_detail(indicator=var,
                                     excel_file=filename,
                                     sheet_name=f'{var} {df.get_vo.Yb}Vin',
                                     start_cell='B2',
                                     weight=self.weight,
                                     ps=ps)


if __name__ == '__main__':
    r = WeovMultiVarGroupReport(
        varlist=['ggei_ggr_net', 'ggei_ggr'],
        vintages=['202407', '202410'],
    )
    r.gen(filename='ggei_ggr_202407.xlsx')