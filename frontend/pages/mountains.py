# Import dependencies
from frontend.pages.frontend_sections.mountain_section import render_mountain_section
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
    render_mountain_section(vars=vars)
