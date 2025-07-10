# Import python dependencies
import streamlit as st

# Import project dependencies
from streamlit_components.ui_components import (
    data_source_badge
)
from functions.data_functions import (
    StravaData,
    Variables
)
from functions.mapping import (
    activity_df_column_map
)

def render_activity_overview(
    data: StravaData,
    vars: Variables
) -> None:
    """
    """
    # Define page title
    st.title('Activity Overview')

    # Render data source metadata badge
    data_source_badge(blob_connection_string=vars.blob_connection_string,
                      container_name='strava',
                      file_name='activity_data.csv')

    # Define column structure
    columns = st.columns([2, 1, 2])

    # Render date range slide bar in first column
    with columns[0]:
        date_range = st.slider(
            label="Select a range of dates:",
            min_value=vars.first_activity_date,
            max_value=vars.current_date,
            value=(vars.first_activity_date, vars.current_date),
            format="MM/YYYY"
        )

    # Render multiselect activity type input inside final column
    with columns[2]:
        # Collect a list of unique activity types
        all_activity_types = data.return_dataframe()['type'].unique().tolist()

        # Create multiselect object for activity type
        selected_activity_types = st.multiselect(
            label='Activity',
            options=all_activity_types,
            default=['Run'])

    # Filter activity type by selected activity types
    data.filter_column_by_list(column_name='type', filter_values=selected_activity_types)

    # Filter data by selected date range
    data.filter_data_by_date_range(min_date=date_range[0],
                                   max_date=date_range[1],
                                   column_name='start_date')

    # Convert distances into km
    data.convert_distance_into_km(column_name='distance')

    # Convert start_date column to datetime type
    data.convert_column_to_datetime(column_name='start_date')

    # Calculate activity moving time (hh:mm)
    data.calculate_moving_time()

    # Map column headers
    data.map_column_header(mapping_dict=activity_df_column_map)

    # Display data in dataframe
    st.dataframe(data=data.return_dataframe(),
                 use_container_width=True,
                 hide_index=True)
