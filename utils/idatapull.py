from imf_datatools import idata_utilities
from fadfpdata import iso_to_ifs, iso_to_cname
import pandas as pd


idata_utilities.PRIVATE = True


# db = 'IMF.RES.WEO:WEO_LIVE'
# ISOcode = 'USA+GBP+CHN'
# varlist = 'PCPI+NGDP_D'
# freq = 'A'
# df_Q = idata_utilities.get_idata_data(db, key=ISOcode+'.'+varlist+'.'+freq, longformat=True)
# df = df_Q.pivot_table(
#     index=['COUNTRY', 'dates'],
#     columns='INDICATOR',
#     values='OBS_VALUE'
# ).reset_index()
#
# df.columns = df.columns.str.lower()
# df = df.rename(columns={'country':'iso'})
# df['year'] = df['dates'].dt.year
# df['ifscode'] = df['iso'].map(iso_to_ifs)
# df['country'] = df['iso'].map(iso_to_cname)



def idatapull(
        meta_dict: dict = None,
        debug: bool = False
):
    """
    Describe the purpose of the function and what it does.

    :param meta_dict: A dictionary that contains metadata information to download different databases.
                      Default values: freq='A', start=None, end=None.
                      Required values: dbname, clist, indlist
    :param debug: If True, the function will print debugging information to help trace its operation.
    :return: A dataframe that combines data from all specified databases.

    Example:
    >>> meta_dict = {
    'Database 1':{
        'dbname': 'WEO_WEO_PUBLISHED',
        'clist': 'USA+GBP',
        'indlist': 'NGDP+NGDPD',
        'freq': 'A',
        'start': 2000,
        'end': 2020
        },
    'Database 2':{
        'dbname': 'ECDATA_BOP',
        'clist': 'USA+GBP',
        'indlist': 'BFD_BP6_USD',
        'freq': 'A',
        'start': 2000,
        'end': 2020
        }
    }
    >>> result = idatapull(meta_dict, debug=True)
    >>> print(result)
    """
    errmsg = ''
    df = pd.DataFrame()
    df['COUNTRY'] = ''
    df['dates'] = ''

    for key in meta_dict.keys():
        dbname = meta_dict[key]['dbname']
        clist = meta_dict[key]['clist']
        indlist = meta_dict[key]['indlist']
        freq = meta_dict[key]['freq']
        start = meta_dict[key]['start'] if 'start' in meta_dict[key].keys() else None
        end = meta_dict[key]['end'] if 'end' in meta_dict[key].keys() else None

        if debug:
            print(
                f'{key}/{len(meta_dict.keys())}: idata_utilities.get_idata_data({dbname}, key={clist}+"."+{indlist}+"."+{freq}, longformat=True)')
        # Only triggered when using EcosSet
        if dbname is not None:
            data = idata_utilities.get_idata_data(dbname, key=fr'{clist}.{indlist}.{freq}', longformat=True)
        else:
            print(f'{key}/{len(meta_dict.keys())}: Skipped, Check Excel Template')
            continue

        ## print notification message including time duration for pulling the data
        if data is not None:
            if start is not None:
                data = data[data['dates'].dt.year >= start]
            if end is not None:
                data = data[data['dates'].dt.year <= end]
            df = pd.concat([df, data])

        else:
            errmsg = errmsg + '\n' + f'{dbname} {indlist} NO data available' + '\n'

    print(errmsg)
    df = df.pivot_table(
        index=['COUNTRY', 'dates'],
        columns='INDICATOR',
        values='OBS_VALUE'
    ).reset_index()

    df.columns = df.columns.str.lower()
    df = df.rename(columns={'country': 'iso'})
    df['country'] = df['iso'].map(iso_to_cname)
    df['ifscode'] = df['iso'].map(iso_to_ifs)
    df['ifscode'] = pd.to_numeric(df['ifscode'], errors='coerce')
    df = df[~df['ifscode'].isna()]
    df['ifscode'] = df['ifscode'].astype(int)
    df['year'] = df['dates'].dt.year
    df.drop(columns='dates', inplace=True)
    df = df.sort_values(['country', 'year'])
    order_cols = ['country','ifscode', 'iso', 'year']
    rest_cols = [c for c in df.columns if c not in order_cols]
    df = df[order_cols + rest_cols]
    return df

if __name__ == '__main__':
    from fadfpdata import ifs_to_iso, Dummy
    clist = '+'.join(str(ifs_to_iso[ifs]) for ifs in Dummy().noagg)
    pull_dict = {
        'Database 1': {
            'dbname': 'IMF.RES.WEO:WEO_LIVE',
            'clist': clist,
            'indlist': 'LP+NGDP_D',
            'freq': 'A',
            'start': 2000,
            'end': 2029
        },
        'Database 2': {
            'dbname': 'IMF.RES.WEO:WEO_LIVE',
            'clist': clist,
            'indlist': 'PCPI+NGDP_DPCH',
            'freq': 'A',
            'start': 2000,
            'end': 2029
        }
    }
    a = idatapull(pull_dict, debug=True)

