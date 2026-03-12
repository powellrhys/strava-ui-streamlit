# Import dependencies
import math

from streamlit_components.ui_components import configure_page_config
from functions.data_functions import StravaData, Variables
from functions.ui_components import render_page_logo
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen
import io
import math

# Set page config
configure_page_config(repository_name='strava-ui-streamlit',
                      page_icon='🏃‍♂️')

# Collect codebase variables
vars = Variables()

# Ensure user is authenticated to use application
if not st.user.is_logged_in:
    st.login('auth0')

if 'buffer' not in st.session_state:
    st.session_state.buffer = io.BytesIO()


@st.cache_data
def load_data(blob_connection_string, container_name, blob_name):
    welsh_peaks_df = StravaData(blob_connection_string=blob_connection_string,
                                container_name=container_name,
                                blob_name=blob_name)
    return welsh_peaks_df.return_dataframe()


@st.cache_data
def build_map(df_json, min_height, counties):
    df = pd.read_json(df_json)
    df = df[df["Feet"] >= min_height]
    if counties:
        df = df[df["County"].isin(counties)]

    if df.empty:
        return None

    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()])
    m.fit_bounds([
        [df["Latitude"].min(), df["Longitude"].min()],
        [df["Latitude"].max(), df["Longitude"].max()]
    ])
    Fullscreen().add_to(m)

    for _, row in df.iterrows():
        color = "green" if row["climbed"] == True else "red"
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                f"<b>{row['Name']}</b><br>"
                f"Height: {row['Metres']}m / {row['Feet']}ft<br>"
                f"County: {row['County']}<br>"
                f"Climbed: {'✅' if row['climbed'] else '❌'}",
                max_width=200,
            ),
            tooltip=row["Name"],
            icon=folium.Icon(color=color, icon="mountain", prefix="fa"),
        ).add_to(m)

    return m


# Render application if user is logged in
if st.user.is_logged_in:

    render_page_logo()
    st.title("Welsh Mountains Map")

    df = load_data(blob_connection_string=vars.blob_connection_string,
                   container_name='strava',
                   blob_name='welsh_peaks_climbed.csv')

    # Filters row
    with st.container(border=False):
        columns = st.columns([3, 1, 2])

        with columns[-1]:
            min_height = st.slider(
                label="Minimum Height (ft)",
                min_value=1000,
                max_value=3600,
                value=3000,
                step=100,
                key="height_slider"
            )

        with columns[0]:
            counties = st.multiselect(
                label="County",
                options=df.County.unique()
            )

    m = build_map(df.to_json(), min_height, tuple(counties))

    # Map row
    with st.container(border=True):
        if m is None:
            st.info("No peaks match the selected filters.")
        else:
            st_folium(m, use_container_width=True, height=400)