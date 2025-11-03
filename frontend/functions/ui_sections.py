# Import dependencies
from streamlit_components.ui_components import data_source_badge
from streamlit_components.plot_functions import PlotlyPlotter
from functions.ui_components import homepage_metrics
from functions.mapping import activity_df_column_map
from functions.data_functions import (
    generate_coastal_path_heatmap,
    sum_coastal_path_distance,
    generate_heatmap,
    StravaData,
    Variables
)
import plotly.express as px
import streamlit as st
import pandas as pd
import datetime

def render_home_page(
    data: StravaData,
    vars: Variables
) -> None:
    """
    Renders the main dashboard page in Streamlit displaying Strava activity statistics.

    This function sets the page title and header, shows yearly distance metrics
    by calling the `homepage_metrics` function, and displays a data source badge
    indicating metadata about the activity data file stored in Azure Blob Storage.

    Args:
        data (StravaData): An instance containing Strava activity data and related methods.
        vars (Variables): An instance containing configuration variables, including current year and storage
            credentials.

    Side Effects:
        Renders Streamlit UI components on the page.
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
    Renders the "Activity Overview" page in Streamlit with interactive filters and
    displays a filtered and formatted table of Strava activity data.

    The page includes:
    - A metadata badge showing data source information.
    - A date range slider to filter activities by start date.
    - A multiselect box to filter activities by type.
    - Data transformations such as distance conversion, datetime formatting,
      moving time formatting, and column renaming.
    - A dynamic table showing the filtered and formatted activity data.

    Args:
        data (StravaData): An instance containing Strava activity data and methods
            for filtering and transformation.
        vars (Variables): An instance containing configuration variables such as
            date boundaries and storage credentials.

    Side Effects:
        - Renders Streamlit UI components (slider, multiselect, dataframe, badges).
        - Modifies `data.df` in-place via filtering and data transformations.
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
    Renders the Heatmap page in Streamlit, allowing users to filter activities by type
    and date range, generate an interactive heatmap of activity routes, and download
    the heatmap as an HTML file.

    Features include:
    - Multi-select filter for activity types.
    - Date inputs for selecting start and end dates.
    - Button to generate the heatmap based on current filters.
    - Download button enabled once the heatmap is generated.
    - Feedback messages and loading spinner during heatmap generation.

    Args:
        data (StravaData): An instance containing Strava activity data and filtering methods.

    Side Effects:
        - Modifies `data.df` via filtering methods.
        - Updates Streamlit session state with generated heatmap HTML.
        - Reruns the app after heatmap generation to refresh UI components.
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
    Renders the Progress Overview page in Streamlit, providing interactive controls
    to visualize Strava activity metrics over time.

    Features include:
    - Conversion of distances from meters to kilometers.
    - Multi-select input to filter activities by type.
    - Selection between bar and line chart types.
    - Choice of metric to visualize (e.g., Distance, Count, Kudos Count, Total Elevation Gain, Moving Time).
    - Plot resolution selector (Yearly or Monthly) affecting aggregation and date slider format.
    - Date range slider to filter data temporally.
    - Aggregation and filtering of activity data based on user inputs.
    - Visualization rendered using Plotly, displayed in the Streamlit app.

    Args:
        data (StravaData): An instance containing Strava activity data and data manipulation methods.

    Side Effects:
        - Modifies `data.df` in-place (distance conversion).
        - Renders multiple Streamlit UI components and interactive plots.
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

    # Collect a unique list of activity types
    unique_types = grouped_df['type'].unique()

    # Handle colour mapping logic
    # Case 1: Only one type
    if len(unique_types) == 1:
        color_discrete_sequence = ["#fc4c02"]

    # Case 2: Multiple types — keep "Run" orange, let Plotly handle the rest
    else:
        # Get Plotly’s default color palette
        default_colors = px.colors.qualitative.Plotly

        # Move "#fc4c02" (Run color) to the front, then fill in others
        color_discrete_sequence = []
        if "Run" in unique_types:
            color_discrete_sequence.append("#fc4c02")

        # Fill remaining types with default colors (excluding the orange if already added)
        remaining_colors = [c for c in default_colors if c.lower() != "#fc4c02"]
        color_discrete_sequence.extend(remaining_colors)

    # Generate plotly plotter object
    plt = PlotlyPlotter(df=grouped_df,
                        x='start_date',
                        y=metric.lower().replace(' ', '_'),
                        color='type',
                        labels={'start_date': 'Date',
                                'type': 'Activity Type',
                                metric.lower().replace(' ', '_'): metric},
                        color_discrete_sequence=color_discrete_sequence,
                        title=f'{plot_resolution} {metric} by Type')

    # Handle which plot to plot
    if chart_type == 'Bar':
        fig = plt.plot_bar()
    if chart_type == 'Line':
        fig = plt.plot_line()

    # Illustrate figure
    st.plotly_chart(fig)

def render_costal_path_page(data: StravaData) -> None:
    """
    Renders the Coastal Path Heatmap page using Streamlit.

    This function:
    - Sets the page title to 'Coastal Path Heatmap'
    - Generates a heatmap based on the provided Strava data
    - Writes the heatmap HTML to a session state buffer
    - Displays a download button to export the heatmap as an HTML file

    Parameters:
    ----------
    data : StravaData
        A structured object containing Strava activity data used to generate the heatmap.

    Returns:
    -------
    None
    """
    # Render Page title
    st.title('Coastal Path Heatmap')

    # Aggregate coastal path data
    wcp_distance, distance_per_year_df = sum_coastal_path_distance(data=data)

    # Define column object
    columns = st.columns(2)

    # Render total distance metric in first column
    with columns[0]:
        st.metric(label="Total Coastal Path Distance Covered", value=f"{wcp_distance} km", border=True)

    # Render percentage of coastal path covered in final column
    with columns[1]:
        st.metric(label="Percentage of coastal path covered",
                  value=f'{format(wcp_distance * 100 / 1400, ",.2f")} %',
                  border=True)

    # Render bar plot of distance covered every year within streamlit container object
    with st.container(border=True):
        st.plotly_chart(
            PlotlyPlotter(
                df=distance_per_year_df,
                x='year',
                y="wcp_value",
                labels={"year": "Year", "wcp_value": "Distance (km)"},
                color_discrete_sequence=["#fc4c02"],
                title="Breakdown of Welsh Coastal Path Progress").plot_bar())

    # Generate coastal path heatmap
    map = generate_coastal_path_heatmap(data=data)

    # Update buffer variable with folium object
    st.session_state.buffer.write(map.encode())
    st.session_state.buffer.seek(0)

    # Render Download Heatmap Button
    st.download_button(
        label="Download Heatmap",
        data=st.session_state.buffer,
        file_name='heatmap.html',
        mime="text/html"
    )
