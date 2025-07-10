# Import python dependencies
from streamlit_components.data_functions import (
    BlobData
)
import streamlit as st
import datetime as dt
import pandas as pd

class Variables:
    """
    Class to collect environmental variables from secrets.toml file. Secrets should
    be located in .streamlit/secrets.toml file

    Args: None

    Raise: None

    Return: None
    """
    def __init__(self):

        # Date related variables
        self.current_year = dt.date.today().year
        self.previous_year = dt.date.today().year - 1
        self.first_activity_date = dt.datetime(2016, 1, 1)
        self.current_date = dt.datetime(dt.datetime.now().year, 12, 31)

        # Collect environmental variables
        self.blob_connection_string = st.secrets['general']['blob_connection_string']

class StravaData(BlobData):
    """
    """
    def filter_data_by_date_range(
        self,
        min_date,
        max_date,
        column_name
    ) -> None:
        """
        """
        self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce').dt.tz_localize(None)
        self.df = self.df[
            (self.df[column_name] >= min_date) & (self.df[column_name] <= max_date)]

    def filter_column_by_list(
        self,
        column_name: str,
        filter_values: list
    ) -> None:
        """
        """
        self.df = self.df[self.df[column_name].isin(filter_values)]

    def convert_distance_into_km(
        self,
        column_name: str = 'distance'
    ) -> None:
        """
        """
        self.df[column_name] = (self.df[column_name] / 1000).round(2)

    def calculate_moving_time(
        self,
        column_name: str = 'moving_time'
    ) -> None:
        """
        """
        self.df[column_name] = self.df[column_name] \
            .apply(lambda x: f"{x // 3600}:{(x % 3600) // 60:02}")

    def map_column_header(
        self,
        mapping_dict: dict
    ) -> None:
        """
        """
        # Rename and select dataframe columns
        self.df = self.df.rename(columns=mapping_dict)
        self.df = self.df[list(mapping_dict.values())]
