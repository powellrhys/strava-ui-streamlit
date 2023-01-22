import os
import webbrowser
import streamlit as st
from dotenv import load_dotenv
from functions.connect import *
from functions.collect_data import *

st.set_page_config(
    initial_sidebar_state="expanded",
    layout="centered"
)

load_dotenv()

def landing_page(data_collected):

    if data_collected is False:
        activity_data = []
    else:
        activity_data = st.session_state['activity_data']

    client_id = st.text_input(
        label="Enter Strava Client ID",
        placeholder="Enter Client ID",
        value=os.getenv('client_id')
        )

    client_secret = st.text_input(
        label="Enter Strava Client Secret",
        placeholder="Enter Client Secret",
        value=os.getenv('client_secret')
    )

    redirect_uri = 'http://localhost:8502/'
    request_url = authorization(client_id, redirect_uri)

    st.markdown(
        f'''
        <a href='{request_url}'><button>Log In to Strava</button></a>
        ''',
        unsafe_allow_html=True
        )

    url_code = st.text_input(
        label="Provide  Access Token from url:",
        placeholder="Value found from redirect url code"
    )

    fetch_data = st.button('Retrieve Strava Data')

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
