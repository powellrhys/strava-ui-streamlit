# Import python dependencies
from folium.plugins import Fullscreen
import streamlit as st
import polyline
import datetime
import folium
import io

# Import project dependencies
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

# Configure page initial state
if 'download_disabled' not in st.session_state:
    st.session_state.download_disabled = True

if 'buffer' not in st.session_state:
    st.session_state.buffer = io.BytesIO()

if not st.session_state['logged_in'] and vars.login_required:

    # Render login component
    login_page()

else:

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
            st.success('HeatMap Ready for Download')

    # Render column 2 components
    with col2:

        # Render start date range input button
        end = st.date_input("End Date", datetime.datetime.today())

    # Define logic for when Generate Heatmap button is clicked
    if generate:

        # Render spinner for when heatmap is being created
        with st.spinner('Generating Heatmap'):

            # Read activity data
            df = read_activity_data(vars=vars)

            # Construct folium object
            m = folium.Map(tiles='cartodb positron', location=[51.4837, 0], zoom_start=6)

            # Iterate through activity data and collect polylines
            for index, row in df.iterrows():

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

            # Reload page
            st.rerun()
