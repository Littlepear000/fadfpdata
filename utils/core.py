import pandas as pd
import pandaspro as cpd
import numpy as np

def weighted_mean(values, weights):
    mask = ~np.isnan(values)
    return np.average(values[mask], weights=weights[mask])