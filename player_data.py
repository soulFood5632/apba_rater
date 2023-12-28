import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class player_data_set:
    def __init__(self, analytics, prev_year):
        """Creates a new player_data_set object.

        :param analytics: The analytics data for the current year.
        :param prev_year: The hbmhl data for the previous year."""
        if type(self.analytics) is str:
            self.analytics = pd.read_csv(self.analytics)
        elif type(self.analytics) is pd.DataFrame:
            self.analytics = analytics
        else:
            raise TypeError("analytics must be a path to a csv file or a pandas DataFrame")

        if type(self.prev_year) is str:
            self.prev_year = pd.read_csv(self.prev_year)
        elif type(self.prev_year) is pd.DataFrame:
            self.prev_year = prev_year
        else:
            raise TypeError("prev_year must be a path to a csv file or a pandas DataFrame")

        self.analytics_list = self.analytics['Name'].unique()
        self.hbmhl_list = self.prev_year['Name'].unique()


