# Import dependencies
from pages.frontend_sections.pb_efforts_section import render_running_pb_section
from streamlit_components.ui_components import configure_page_config
from functions.data_functions import StravaData, Variables
from functions.ui_components import render_page_logo
import streamlit as st

# Set page config
configure_page_config(repository_name='play-cricket',
                      page_icon='🏃‍♂️')

# Collect codebase variables
vars = Variables()

# Ensure user is authenticated to use application
if not st.user.is_logged_in:
    st.login('auth0')

# Render application if user is logged in
if st.user.is_logged_in:

    # Render page logo
    render_page_logo()

    pb_effort_data = StravaData(blob_connection_string=vars.blob_connection_string,
                                container_name='strava',
                                blob_name='pb_effort_data.csv')

    render_running_pb_section(data=pb_effort_data)
