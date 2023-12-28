import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def data_histogram(hb_dataframe: pd.DataFrame, stat: str, bins: int):
    """Creates a histogram of the provided dataset.

    :param hb_dataframe: A dataframe containing the hb data.
    :param stat: The state who would like to see a histogram of.
    :param bins: The number of bins to be used in the histogram.
    :returns: A histogram of the data."""
    if stat not in hb_dataframe.columns:
        raise KeyError("The stat you are looking for is not in the dataframe")
    plt.hist(hb_dataframe[stat].values, bins=bins)
    plt.show()


