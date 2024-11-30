import os
import pandas as pd


def load_all_apba():
    """ Loads all the hb_data from the apba folder and prepares it as a pandas dataframe with the year. """
    all_apba = pd.DataFrame()
    # gets the list of all files in the apba folder.
    for file in os.listdir("data/apba_data"):
        # this should never be false
        if file.endswith(".csv"):
            # the year is in the last two digits of the file name beofre the .csv
            year = file.split(".")[0][-2:]
            year_data = pd.read_csv("data/apba_data/" + file)
            year_data["season"] = f"{int(year) - 1}-{year}"

            all_apba = all_apba._append(year_data, ignore_index=True)
    all_apba = __filter_cols(all_apba)

    return all_apba


def load_hr(years):
    hr = pd.DataFrame()
    for year in years:
        year_data = pd.read_csv("data/hockey_ref/" + year + '_CompleteData' + ".csv")
        # TODO: change this logic to be of better style
        hr = hr._append(year_data, ignore_index=True)

    return hr


def __filter_cols(df: pd.DataFrame):
    """Filters the columns of the apba data so that the columns for First, Last, year, and any rating columns remain."""
    full_names = []

    for first, last in zip(df["First"], df["Last"]):
        if "." in last:
            last = last.split(".")[1].strip()
        full_names.append(f"{first} {last}")

    df["Player"] = full_names
    df["RateLWDefence"] = df["RateLWDefense"]
    df["RateRWDefence"] = df["RateRwDefence"]
    df = df.drop(columns=["RateLWDefense", "RateRwDefence"])

    good_cols = ['Player', 'season']
    good_cols += [col for col in df.columns if col.startswith("Rate")]

    return df.filter(items=good_cols)
