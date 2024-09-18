import imf_datatools
import pandas as pd


def myecosuse(
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
        'clist': [111, 112],
        'indlist': ['NGDP', 'NGDPD'],
        'freq': 'A',
        'start': 2000,
        'end': 2020
        },
    'Database 2':{
        'dbname': 'ECDATA_BOP',
        'clist': [111, 112],
        'indlist': 'BFD_BP6_USD',
        'freq': 'A',
        'start': 2000,
        'end': 2020
        }
    }
    >>> result = myecosuse(meta_dict, debug=True)
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
                f'{key}/{len(meta_dict.keys())}: imf_datatools.get_ecos_sdmx_data({dbname}, {clist}, {indlist}, freq={freq}, longformat=True)')
        # Only triggered when using EcosSet
        if dbname is not None:
            data = imf_datatools.get_ecos_sdmx_data(dbname, clist, indlist, freq=freq, longformat=True)
        else:
            print(f'{key}/{len(meta_dict.keys())}: Skipped, Check Excel Template')
            continue

        ## print notification message including time duration for pulling the data
        if data is not None:
            if start is not None:
                data = data[data['dates'].dt.year >= start]
            if end is not None:
                data = data[data['dates'].dt.year <= end]
            df = pd.merge(df, data, on=['COUNTRY', 'dates'], how='outer')

        else:
            errmsg = errmsg + '\n' + f'{dbname} {indlist} NO data available' + '\n'

    print(errmsg)
    df.rename(columns={'COUNTRY': 'ifscode'}, inplace=True)
    df['ifscode'] = df['ifscode'].astype(int)
    df['year'] = df['dates'].dt.year
    # df.drop(columns='dates', inplace=True)
    new_order = ['ifscode', 'year', 'dates'] + [col for col in df.columns if col not in ['ifscode', 'year', 'dates']]  # reorder the columns
    return df[new_order]

if __name__ == '__main__':
    pull_dict = {
        'Database 1': {
            'dbname': 'WEO_WEO_LIVE',
            'clist': [110, 1201],
            'indlist': ['GGXCNL_GDP'],
            'freq': 'A',
            'start': 2000,
            'end': 2029
        }
    }
    a = myecosuse(pull_dict, debug=True)

