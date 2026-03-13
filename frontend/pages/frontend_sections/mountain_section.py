# Import dependencies
from functions.data_functions import load_and_cache_data, Variables, build_mountain_map
from streamlit_folium import st_folium
import streamlit as st

def render_mountain_section(vars: Variables) -> None:
    """
    Renders the mountain section of the application, which includes a map
    of welsh peaks climbed based on user-selected filters.
    """
    # Render page title
    st.title("Welsh Peaks Climbing Overview")

    # Load welsh peak data
    df = load_and_cache_data(
        blob_connection_string=vars.blob_connection_string,
        container_name='strava',
        blob_name='welsh_peaks_climbed.csv')

    # Render filters within container
    with st.container(border=True):
        columns = st.columns([3, 1, 2])

        # Render county multiselect in left column
        with columns[0]:
            counties = st.multiselect(
                label="County",
                options=df.County.unique()
            )

        # Render height slider in middle column
        with columns[-1]:
            min_height = st.slider(
                label="Minimum Height (ft)",
                min_value=2000,
                max_value=3600,
                value=3000,
                step=100,
                key="height_slider"
            )

    # Build map based on filters
    m = build_mountain_map(df.to_json(), min_height, tuple(counties))

    # Map row
    with st.container(border=True):
        if m is None:
            st.info("No peaks match the selected filters.")
        else:
            st_folium(m, use_container_width=True, height=400)
