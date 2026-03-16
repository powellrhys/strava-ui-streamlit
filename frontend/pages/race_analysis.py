# Import dependencies
from pages.frontend_sections.running_race_analysis import render_running_race_analysis_section
from streamlit_components.ui_components import configure_page_config
from functions.data_functions import Variables
import streamlit as st

# Set page config
configure_page_config(repository_name='strava-ui-streamlit',
                      page_icon='🏃‍♂️')

# Collect codebase variables
vars = Variables()

# Ensure user is authenticated to use application
if not st.user.is_logged_in:
    st.login('auth0')

# Render application if user is logged in
if st.user.is_logged_in:

    # Render page section
    render_running_race_analysis_section()