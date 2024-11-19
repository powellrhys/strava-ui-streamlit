import streamlit as st
import pandas as pd

from functions.ui_components import \
    configure_page_config, \
    login_page

from functions.collect_data import \
    read_activity_data

from functions.variables import \
    Variables

# Setup page config
configure_page_config()

# Load page variables
vars = Variables()


if not st.session_state['logged_in'] and vars.login_required:

    # Render login component
    login_page()

else:

    # Read in activity data
    activity_data = read_activity_data(vars=vars)

    # Drop index when reading in data from csv
    activity_data = activity_data.drop([activity_data.columns[0]], axis=1)

    # Collect a list of unique activity types
    all_activity_types = activity_data['type'].unique().tolist()

    # Define page title
    st.title('Activity Overview')

    # Create a slider with two datetime values
    date_range = st.sidebar.slider(
        label="Select a range of dates:",
        min_value=vars.first_activity_date,
        max_value=vars.current_date,
        value=(vars.first_activity_date, vars.current_date),
        format="MM/YYYY"
    )

    # Create multiselect object for activity type
    selected_activity_types = st.sidebar \
        .multiselect(label='Activity',
                     options=all_activity_types,
                     default=['Run'])

    # Filter data by activity type
    activity_data = activity_data[activity_data['type'].isin(selected_activity_types)]

    # Filter by date range
    activity_data['start_date'] = activity_data['start_date'].dt.tz_localize(None)
    activity_data = activity_data[
        (activity_data['start_date'] >= date_range[0]) & (activity_data['start_date'] <= date_range[1])]

    # Convert distance from meters to kilometers
    activity_data['distance'] = (activity_data['distance'] / 1000).round(2)

    # Convert start date column in date format (remove the time element)
    activity_data['start_date'] = pd.to_datetime(activity_data['start_date']).dt.date

    # Convert moving time data to hh:mm format
    activity_data['moving_time'] = activity_data['moving_time'] \
        .apply(lambda x: f"{x // 3600}:{(x % 3600) // 60:02}")

    # Column Mapping
    column_headers_map = {
        'name': 'Name',
        'distance': 'Distance (km)',
        'moving_time': 'Moving Time (hh:mm)',
        'total_elevation_gain': 'Elevation Gain (m)',
        'type': 'Activity Type',
        'start_date': 'Date',
        'kudos_count': 'Kudos Count'
    }

    # Rename and select dataframe columns
    activity_data = activity_data.rename(columns=column_headers_map)
    activity_data = activity_data[list(column_headers_map.values())]

    # Display data in dataframe
    st.dataframe(data=activity_data,
                 use_container_width=True,
                 hide_index=True)
