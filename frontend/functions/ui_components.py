# Import python dependencies
import streamlit as st
import pandas as pd

# Import project functions
from functions.data_functions import (
    Variables
)

def homepage_metrics(activity_data: pd.DataFrame,
                     vars: Variables) -> None:
    """
    Generates and displays a homepage metrics component in Streamlit summarizing
    activity data over the current and previous years for selected activity types.

    The function calculates the total distance (in kilometers) and number of entries
    for each activity type ('Run', 'Ride', 'Swim', 'Golf', 'Walk') across two years,
    then visualizes the current year's distance along with the difference compared
    to the previous year using Streamlit metric components.

    Args:
        activity_data (pd.DataFrame): DataFrame containing Strava activity data,
            expected to have 'type', 'start_date', and 'distance' columns.
        vars (Variables): An instance containing date-related variables such as current
            and previous year.
    """
    # Define activity types of interest
    activity_types = ['Run', 'Ride', 'Swim', 'Golf', 'Walk']
    activity_data['start_date'] = pd.to_datetime(activity_data['start_date'], errors='coerce')

    # Iterate through all activity types to get the previous 2 years of data
    data = {}
    for type in activity_types:

        # Collect yearly data
        yearly_data = {}
        for year in [vars.current_year, vars.previous_year]:

            filtered_df = activity_data[(activity_data['type'] == type) & (activity_data['start_date'].dt.year == year)]

            yearly_data[year] = {
                'entries': len(filtered_df),
                'distance': filtered_df['distance'].sum()/1000
            }

            # Append yearly data to dictionary
            data[type] = yearly_data

    # Define columns
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    # Iterate through columns to create metric components
    for i in range(len(columns)):

        # Calculate the difference in distance between this year and last year
        diff = data[activity_types[i]][vars.current_year]['distance'] - \
            data[activity_types[i]][vars.previous_year]['distance']

        # Render metric components
        with columns[i]:
            st.metric(label=activity_types[i],
                      value=f"{round(data[activity_types[i]][2024]['distance'], 2)} km",
                      delta=f"{round(diff, 2)} km"
                      )
