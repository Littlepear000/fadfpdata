from imf_datatools import idata_utilities

# Get public databases
datasets = idata_utilities.get_databases()

# To get non-public datasets, set PRIVATE to True.
idata_utilities.PRIVATE = True
datasets_all = idata_utilities.get_databases(refresh=True)