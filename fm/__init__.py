import pandas as pd
import numpy as np
import pandaspro as cpd
from fadfpdata.myclass.dummy import Dummy
from fadfpdata.myclass.ecosdata import EcosData
from fadfpdata.utils.core import cname_to_ifs, ifs_to_cname, iso_to_ifs

# fm_version = '2025-10'
# fm_folder_name = 'October-Monitor'
# curr_year = int(fm_version[:4])
# curr_mon = int(fm_version[-2:])
# fm_folder = f'{fm_version}-{fm_folder_name}'
# input_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA\input sources'
# output_folder = fr'Q:\DATA\FP\Fiscal Monitor\{fm_folder}\MSA'
# blmbg_update_date = '20250916'
# wbnrh_update_date = '20250916'
# weo_update_date = '20250916'
# ep_update_date = '20250820'
# ep_start_year = 2024

ecos = EcosData()
dum = Dummy()
