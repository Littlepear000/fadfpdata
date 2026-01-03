from fadfpdata.utils.core import ifs_to_iso
from fadfpdata.myclass.dummy import Dummy
import fadfpdata.downloads.idata.config as c
from fadfpdata.downloads import idata_root
from fadfpdata.utils.idatapull import idatapull
from openpyxl.utils import column_index_from_string, get_column_letter
import xlwings as xw
import os
import shutil
import datetime
import time

folder_weolive = f'{idata_root}/WEOlive'

# Step 1: read excel of Data Pulling Tool Main Dashboard
# Step 2: retrieve the meta info into a dictionary
# Step 3: parse dictionary and use it with imf_datatools to download data

def _update_log(timestamp, logdict):
    log_entry = f"{timestamp}\n===========================\n{str(logdict)}\n"
    log_file_path = os.path.join(folder_weolive, 'templates', 'log.txt')

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            lines = file.readlines()

        entry_index = None
        end_index = None
        for i, line in enumerate(lines):
            if line.strip() == timestamp:
                entry_index = i
            elif entry_index is not None and line.strip() and line.strip().isdigit() and len(line.strip()) == 8:
                end_index = i - 1
                break

        if entry_index is not None and end_index is not None:
            lines = lines[:entry_index] + [log_entry] + lines[end_index:]
        elif entry_index is not None:
            lines = lines[:entry_index] + [log_entry]
        else:
            lines.append(log_entry)
    else:
        lines = [log_entry]

    with open(log_file_path, 'w') as file:
        file.writelines(lines)


class iDataSet:
    def __init__(
            self,
            workbook: str = 'Data Pulling Template.xlsx',
            update: bool = True
    ):
        if update:
            today = datetime.datetime.today().strftime('%Y%m%d')
            template_file = c.template
            destination_file = os.path.join(f'{idata_root}/WEOlive/templates', f'template_{today}.xlsx')
            shutil.copyfile(template_file, destination_file)
            self.path = destination_file
        else:
            destination_file = os.path.join(os.getcwd(), workbook)
            if os.path.exists(destination_file):
                print(f'Opening current {workbook} in the folder ... ')
            else:
                # noinspection PyUnboundLocalVariable
                shutil.copyfile(c.template, destination_file)
                print(f'{workbook} copied from template into the folder ... ')
            self.path = os.path.join(os.getcwd(), workbook)

        wb = xw.Book(self.path)
        ws = wb.sheets['Dashboard']
        sectioncol = ['B', 'F', 'J', 'N', 'R']

        pull_dict = {}
        for index, col in zip(range(5), sectioncol):
            pull_dict[f'Database {index + 1}'] = {}
            dbname = ws.range(f'{col}3').value
            colindex = column_index_from_string(col)

            freq = ws.range(f'{col}4').value
            start = ws.range(f'{col}5').value
            end = ws.range(f'{col}6').value
            countryselect = ws.range(f'{col}7').value

            if countryselect == 'All countries w/o aggregates':
                clist = '+'.join(str(ifs_to_iso[ifs]) for ifs in Dummy().noagg)
            elif countryselect == 'All countries w aggregates':
                clist = '+'.join(str(ifs_to_iso[ifs]) for ifs in Dummy().noagg)
            else:
                clist_colindex = colindex - 1
                clist_col = get_column_letter(clist_colindex)
                clist_raw = [int(country) for country in ws.range(f'{clist_col}10:{clist_col}209').value if
                             country is not None and str(country).strip() != '']
                clist_ifs = [country for country in clist_raw if
                             isinstance(country, (int, float)) or (isinstance(country, str) and country.isdigit())]
                #clist_iso = [c for c in clist_raw if isinstance(c, str) and re.match('[A-Z]{3}', c)]
                clist = clist_ifs
                ###############################################
                # Future update: match iso and name to ifscode
                ###############################################

            #counterlist = [c for c in ws.range(f'{col}10:{col}209').value if c is not None]
            indlist_colindex = colindex + 1
            indlist_col = get_column_letter(indlist_colindex)
            indlist = [i for i in ws.range(f'{indlist_col}10:{indlist_col}209').value if i is not None]
            indlist = '+'.join(ind for ind in indlist)

            pull_dict[f'Database {index + 1}']['dbname'] = dbname
            pull_dict[f'Database {index + 1}']['clist'] = clist
            pull_dict[f'Database {index + 1}']['indlist'] = indlist
            pull_dict[f'Database {index + 1}']['freq'] = freq
            pull_dict[f'Database {index + 1}']['start'] = start
            pull_dict[f'Database {index + 1}']['end'] = end

        self.pull_dict = pull_dict

    def pull(self, export: bool = False, debug: bool = False):
        starttime = time.time()
        data = idatapull(
            meta_dict=self.pull_dict,
            debug=debug
        )
        data.columns = data.columns.str.lower().str.replace('.a', '', regex=False)

        if export:
            timestamp = datetime.datetime.now().strftime('%Y%m%d')
            _update_log(timestamp=timestamp, logdict=self.pull_dict)
            data.to_csv(os.path.join(folder_weolive, f'idata_{timestamp}.csv'), index=False)
            endtime = time.time()
            print(f'Download completed. Time Duration: {round((endtime-starttime)/60, 1)}min')
        else:
            return data

if __name__ == '__main__':
    a = iDataSet()
    a.pull(export=True, debug=True)
