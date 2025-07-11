# Import python dependencies
import streamlit as st
import pandas as pd
import datetime

# Import project dependencies
from streamlit_components.plot_functions import (
    PlotlyPlotter
)
from streamlit_components.ui_components import (
    data_source_badge
)
from functions.data_functions import (
    generate_heatmap,
    StravaData,
    Variables
)
from functions.ui_components import (
    homepage_metrics
)
from functions.mapping import (
    activity_df_column_map
)

def render_home_page(
    data: StravaData,
    vars: Variables
) -> None:
    """
    """
    # Define page title and header
    st.title('STRAVA DASHBOARD')
    st.header(f'Yearly distance stats to date ({vars.current_year})')

    # Render homepage metrics ui component
    homepage_metrics(activity_data=data.return_dataframe(),
                     vars=vars)

    # Render data source metadata badge
    data_source_badge(blob_connection_string=vars.blob_connection_string,
                      container_name='strava',
                      file_name='activity_data.csv')

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

def render_heatmap(
    data: StravaData
) -> None:
    """
    """
    # Define Page Header
    st.title('Heatmap')

    # Render activity type multiselect component
    options = st.multiselect("Activity Type",
                             ["Run", "Ride", "Walk", "Swim", "Golf"],
                             ["Run", "Ride", "Walk", "Swim", "Golf"])

    # Define 2 columns
    col1, col2 = st.columns(2)

    # Render column 1 components
    with col1:

        # Render start date range input button
        start = st.date_input("Start Date", datetime.date(2016, 1, 1))

        # Render Generate Heatmap Button
        generate = st.button("Generate Heatmap")

        # Render Download Heatmap Button
        st.download_button(
            label="Download Heatmap",
            data=st.session_state.buffer,
            file_name='heatmap.html',
            mime="text/html",
            disabled=st.session_state.download_disabled
        )

        # Render success component if download is possible
        if not st.session_state.download_disabled:
            st.success('Heatmap Ready for Download')

    # Render column 2 components
    with col2:

        # Render start date range input button
        end = st.date_input("End Date", datetime.datetime.today())

    data.filter_column_by_list(column_name='type', filter_values=options)
    data.filter_data_by_date_range(min_date=start, max_date=end, column_name='start_date')

    # Define logic for when Generate Heatmap button is clicked
    if generate:

        # Render spinner for when heatmap is being created
        with st.spinner('Generating Heatmap'):

            generate_heatmap(data=data)

            # Reload page
            st.rerun()

def render_progress_page(
    data: StravaData
) -> None:
    """
    """
    data.convert_distance_into_km(column_name='distance')
    # Convert distance from meters to kilometers
    # activity_data['distance'] = activity_data['distance'] / 1000

    # Collect a list of unique activity types
    all_activity_types = data.return_dataframe()['type'].unique().tolist()

    # Render page title
    st.title('Progress Overview')

    # Define the range for the slider
    start_date = datetime.datetime(2016, 1, 1)
    end_date = datetime.datetime(datetime.datetime.now().year, 12, 31)

    columns = st.columns([2, 2, 1, 3])

    # Render activity type and chart type inputs in column 1
    with columns[0]:
        selected_activity_type = st.multiselect(label='Activity Type',
                                                options=all_activity_types,
                                                default=['Run'])

        # Chart type radio input
        chart_type = st.segmented_control(label='Plot Type',
                                          options=['Bar', 'Line'],
                                          default='Bar')

    # Render metric and plot resolution inputs within column 2
    with columns[1]:
        metric = st.selectbox(label='Metric',
                              options=[
                                  'Distance',
                                  'Count',
                                  'Kudos Count',
                                  'Total Elevation Gain',
                                  'Moving Time'])

        plot_resolution = st.segmented_control(label='Plot Resolution',
                                               options=['Yearly', 'Monthly'],
                                               default='Yearly')

        # Map granularity input to chart resolution
        if plot_resolution == 'Yearly':
            resolution = 'Y'
            date_slider_format = 'YYYY'
        elif plot_resolution == 'Monthly':
            resolution = 'M'
            date_slider_format = 'MM/YYYY'

    # Render date slider component in final column
    with columns[3]:
        date_range = st.slider(
            label="Select a range of dates:",
            min_value=start_date,
            max_value=end_date,
            value=(start_date, end_date),
            format=date_slider_format
        )

    df = data.return_dataframe()
    df['start_date'] = pd.to_datetime(df['start_date'])

    if metric == 'Count':
        grouped_df = df \
            .groupby([df['start_date'].dt.to_period(resolution), 'type'])['type'] \
            .count().reset_index(name='count')

    # Aggregate data by distance
    else:
        grouped_df = df \
            .groupby([df['start_date'].dt.to_period(resolution), 'type']) \
            .sum(numeric_only=True).reset_index()

    # Filter by activity type
    grouped_df = grouped_df[grouped_df['type'].isin(selected_activity_type)]

    # Convert 'date' back to datetime for plotting purposes
    grouped_df['start_date'] = grouped_df['start_date'].dt.to_timestamp()

    # Filter by date range
    grouped_df = grouped_df[
        (grouped_df['start_date'] >= date_range[0]) & (grouped_df['start_date'] <= date_range[1])]

    plt = PlotlyPlotter(df=grouped_df,
                        x='start_date',
                        y=metric.lower().replace(' ', '_'),
                        color='type',
                        labels={'start_date': 'Date',
                                'type': 'Activity Type',
                                metric.lower().replace(' ', '_'): metric},
                        title=f'{plot_resolution} {metric} by Type')

    if chart_type == 'Bar':
        fig = plt.plot_bar()
    if chart_type == 'Line':
        fig = plt.plot_line()

    # Illustrate figure
    st.plotly_chart(fig)
