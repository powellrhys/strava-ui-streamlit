import webbrowser
import streamlit as st
from functions.connect import *
from functions.collect_data import *

st.set_page_config(
    initial_sidebar_state="expanded",
    layout="centered"
)

def landing_page(data_collected):

    if data_collected is False:
        activity_data = []
    else:
        activity_data = st.session_state['activity_data']

    client_id = st.text_input(
        "Enter Strava Client ID",
        "93139"
    )

    client_secret = st.text_input(
        "Enter Strava Client Secret",
        "dbd936b625c579396f069fb928b337a618b7212c"
    )

    clicked = st.button('Log In to Strava')

    url_code = st.text_input(
    "Provide  Access Token from url:"
    )

    fetch_data = st.button('Retrieve Strava Data')

    if clicked:

        redirect_uri = 'http://localhost/'
        request_url = authorization(client_id, redirect_uri)
        webbrowser.open(request_url)


    if fetch_data:

        with st.spinner('Collecting Data...'):
            access_token = get_access_token(client_id, client_secret, url_code)

            for page_number in range(1, 11):
                page_data = get_data(access_token, page=page_number)
                if page_data == []:
                    break
                activity_data = activity_data + page_data

        st.success("All Activity Data Collected")

    return activity_data

if 'activity_data' not in st.session_state:
    st.session_state.activity_data = landing_page(data_collected=False)
else:
    st.session_state.activity_data = landing_page(data_collected=True)
