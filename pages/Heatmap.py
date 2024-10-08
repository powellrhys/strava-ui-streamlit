import folium
import polyline
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import Fullscreen
import datetime
import io

from functions.ui_components import \
    configure_page_config

from functions.collect_data import \
    read_activity_data

# Setup page config
configure_page_config()

if 'download_disabled' not in st.session_state:
    st.session_state.download_disabled = True

print(st.session_state.download_disabled)

if 'buffer' not in st.session_state:
    st.session_state.buffer = io.BytesIO()

st.title('Heatmap')
options = st.multiselect("Activity Type",
                         ["Run", "Ride", "Walk", "Swim", "Golf"],
                         ["Run", "Ride", "Walk", "Swim", "Golf"]
                         )

col1, col2 = st.columns(2)

with col1:

    start = st.date_input("Start Date", datetime.date(2016, 1, 1))
    generate = st.button("Generate Heatmap")

with col2:
    end = st.date_input("End Date", datetime.datetime.today())
    # Provide the download button in Streamlit
    st.download_button(
        label="Download Heatmap",
        data=st.session_state.buffer,
        file_name='heatmap.html',
        mime="text/html",
        disabled=st.session_state.download_disabled
    )

if generate:

    df = read_activity_data()

    m = folium.Map(tiles='cartodb positron', location=[51.4837, 0], zoom_start=6)

    for index, row in df.iterrows():

        try:
            if row['distance'] > 0:
                curve = row['map']

                data = polyline.decode(curve)

                folium.PolyLine(data,
                                color='#fc4c02',
                                weight=1,
                                opacity=0.7).add_to(m)

        except BaseException:
            pass

    Fullscreen(position="topleft").add_to(m)
    # st_folium(m, width=500, height=200, returned_objects=[])

    map_html = m._repr_html_()

    # st.session_state.buffer = io.BytesIO()
    st.session_state.buffer.write(map_html.encode())
    st.session_state.buffer.seek(0)

    st.session_state.download_disabled = False

    # Reload page
    st.rerun()

    # # Provide the download button in Streamlit
    # st.download_button(
    #     label="Download Map",
    #     data=buffer,
    #     file_name='heatmap.html',
    #     mime="text/html"
    # )

    # html_file = io.BytesIO()
    # m.save(html_file)
    # html_file.seek(0)

        # # Provide a download button for the in-memory HTML content
        # st.download_button(
        #     label="Download Map as HTML",
        #     data=html_file.getvalue(),
        #     file_name="map.html",
        #     mime="text/html"
        # )




# print(st.session_state['activity_data'])

# def heatmap_page(activity_data):

#     m = folium.Map(tiles='cartodb positron', location=[51.4837, 0], zoom_start=6)

#     for i in range(len(activity_data)):

#         try:

#             if activity_data[i]["distance"] != 0:

#                 curve = activity_data[i]["map"]["summary_polyline"]

#                 data = polyline.decode(curve)

#                 folium.PolyLine(data,
#                                 color='#fc4c02',
#                                 weight=1,
#                                 opacity=0.3).add_to(m)
#         except BaseException:
#             pass

#     st_folium(m, width=2000, returned_objects=[])


# heatmap_page(st.session_state.activity_data)
