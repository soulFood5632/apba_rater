import os
import pandas as pd


def load_all_apba(dir: str):
    """ loads all the hb_data from the apba folder and prepares it as a pandas dataframe with the year. """
    all_apba = pd.DataFrame()
    # gets the list of all files in the apba folder.
    for file in os.listdir(dir + "apba_data"):
        # this should never be false
        if file.endswith(".csv"):
            # the year is in the last two digits of the file name beofre the .csv
            year = file.split(".")[0][-2:]
            year_data = pd.read_csv("apba_data/" + file)
            year_data["year"] = year

            all_apba = all_apba._append(year_data, ignore_index=True)
    all_apba = __filter_cols(all_apba)

    return all_apba


def load_hr(years):
    hr = pd.DataFrame()
    for year in years:
        year_data = pd.read_csv("HockeyRef_Data_Files/" + year + '_CompleteData' + ".csv")
        hr = hr._append(year_data, ignore_index=True)

    return hr


def __filter_cols(df: pd.DataFrame):
    """Filters the columns of the dataframe to only include the relevant columns"""

    good_cols = ['Last', 'First', 'year']
    good_cols += [col for col in df.columns if col.startswith("Rate")]

    return df.filter(items=good_cols)
