import pandasdmx as sdmx
import pandas as pd

provider = sdmx.Request()
url = 'https://api.imf.org/external/sdmx/2.1'
provider.source.url = url

#define header for request
header = {'User-Agent': 'idata-script-client'}

#retrive data
data_msg = provider.data(
    'WEO',
    key='CHN+USA.NGDP_RPCH+NGDP.A',
    params={'startPeriod': 2000},
    headers=header
)

cpi_df = data_msg.to_pandas().unstack()

