import folium
import polyline
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide"
)

def heatmap_page(activity_data):

    m = folium.Map(tiles='cartodb positron', location=[51.4837, 0], zoom_start= 6)

    for i in range(len(activity_data)):

        try:

            if activity_data[i]["distance"] != 0:

                curve = activity_data[i]["map"]["summary_polyline"]

                data = polyline.decode(curve)
                df = pd.DataFrame(data, columns=['lat','lon'])

                folium.PolyLine(data,
                                color='#fc4c02',
                                weight=1,
                                opacity=0.3).add_to(m)
        except:
            pass

    st_folium(m, width=2000, returned_objects=[])

heatmap_page(st.session_state.activity_data)