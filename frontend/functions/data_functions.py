# Import python dependencies
from streamlit_components.data_functions import (
    BlobData
)
from folium.plugins import Fullscreen
import streamlit as st
import datetime as dt
import pandas as pd
import polyline
import folium

class Variables:
    """
    Loads configuration and environment variables from the `.streamlit/secrets.toml` file.

    This class centralizes access to important constants such as date parameters and
    sensitive credentials like the Azure Blob Storage connection string.

    Attributes:
        current_year (int): The current calendar year.
        previous_year (int): The previous calendar year.
        first_activity_date (datetime): The fixed start date for activities (January 1, 2016).
        current_date (datetime): The end of the current year (December 31).
        blob_connection_string (str): Azure Blob Storage connection string loaded from secrets.
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
    A subclass of BlobData tailored for handling Strava-specific data operations.

    This class can be extended to include methods and properties
    specific to fetching, processing, and managing Strava activity data.
    """
    def filter_data_by_date_range(
        self,
        min_date: str,
        max_date: str,
        column_name: str
    ) -> None:
        """
        Filters the DataFrame in-place to include only rows where the specified date column
        falls within the given date range.

        Converts the `min_date` and `max_date` parameters, as well as the target column,
        to datetime objects (removing any timezone information) before applying the filter.

        Args:
            min_date (str): The start date (inclusive) of the filter range, in a format parsable by pandas.
            max_date (str): The end date (inclusive) of the filter range, in a format parsable by pandas.
            column_name (str): The name of the date column in the DataFrame to filter on.

        Returns:
            None: The filtering is done in-place, modifying `self.df`.
        """
        min_date = pd.to_datetime(min_date)
        max_date = pd.to_datetime(max_date)

        self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce').dt.tz_localize(None)
        self.df = self.df[
            (self.df[column_name] >= min_date) & (self.df[column_name] <= max_date)]

    def filter_column_by_list(
        self,
        column_name: str,
        filter_values: list
    ) -> None:
        """
        Filters the DataFrame in-place to include only rows where the specified column's values
        are present in the given list of filter values.

        Args:
            column_name (str): The name of the column to filter.
            filter_values (list): A list of values to keep in the column.

        Returns:
            None: The filtering modifies `self.df` in-place.
        """
        self.df = self.df[self.df[column_name].isin(filter_values)]

    def convert_distance_into_km(
        self,
        column_name: str = 'distance'
    ) -> None:
        """
        Converts distance values in the specified column from meters to kilometers,
        rounding to two decimal places.

        Args:
            column_name (str): The name of the distance column to convert. Defaults to 'distance'.

        Returns:
            None: The conversion is applied in-place to `self.df`.
        """
        self.df[column_name] = (self.df[column_name] / 1000).round(2)

    def calculate_moving_time(
        self,
        column_name: str = 'moving_time'
    ) -> None:
        """
        Converts moving time values from seconds into a formatted string "H:MM".

        Args:
            column_name (str): The name of the column containing moving time in seconds.
                            Defaults to 'moving_time'.

        Returns:
            None: The conversion is applied in-place to `self.df`.
        """
        self.df[column_name] = self.df[column_name] \
            .apply(lambda x: f"{x // 3600}:{(x % 3600) // 60:02}")

    def map_column_header(
        self,
        mapping_dict: dict
    ) -> None:
        """
        Renames columns in the DataFrame according to the provided mapping dictionary,
        and reorders the DataFrame to include only the renamed columns.

        Args:
            mapping_dict (dict): A dictionary where keys are current column names and values are new column names.

        Returns:
            None: The DataFrame `self.df` is modified in-place.
        """
        # Rename and select dataframe columns
        self.df = self.df.rename(columns=mapping_dict)
        self.df = self.df[list(mapping_dict.values())]

def generate_heatmap(
    data: StravaData
) -> None:
    """
    Generates an interactive folium heatmap of Strava activity routes and updates
    the Streamlit session state with the map HTML for display and download.

    The function decodes GPS polylines from Strava activity data and plots them on
    a map centered around a fixed location. Activities with zero distance or invalid
    data are ignored. Fullscreen control is added to the map.

    Args:
        data (StravaData): An instance containing Strava activity data with decoded polylines.

    Side Effects:
        - Writes the generated map HTML to `st.session_state.buffer`.
        - Enables the download button by setting `st.session_state.download_disabled` to False.
    """
    # Construct folium object
    m = folium.Map(tiles='cartodb positron', location=[51.4837, 0], zoom_start=6)

    # Iterate through activity data and collect polylines
    for _, row in data.return_dataframe().iterrows():

        try:
            # Filter out activities with no gps data
            if row['distance'] > 0:

                # Collect polyline data
                curve = row['map']

                # Decode polyline data
                data = polyline.decode(curve)

                # Add polyline data to folium object
                folium.PolyLine(data,
                                color='#fc4c02',
                                weight=1,
                                opacity=0.7).add_to(m)

        except BaseException:
            pass

    # Add full screen functionality to folium object
    Fullscreen(position="topleft").add_to(m)

    # Convert to html format
    map_html = m._repr_html_()

    # Update buffer variable with folium object
    st.session_state.buffer.write(map_html.encode())
    st.session_state.buffer.seek(0)

    # Make download available
    st.session_state.download_disabled = False
