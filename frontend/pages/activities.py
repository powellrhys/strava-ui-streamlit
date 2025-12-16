# Import python dependencies
import streamlit as st

# Import project dependencies
from streamlit_components.ui_components import (
    configure_page_config,
)
from functions.data_functions import (
    StravaData,
    Variables
)
from functions.ui_components import (
    render_page_logo
)
from functions.ui_sections import (
    render_activity_overview
)

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

    # Render page logo
    render_page_logo()

    activity_data_df = StravaData(blob_connection_string=vars.blob_connection_string,
                                  container_name='strava',
                                  blob_name='activity_data.csv')

    # Render activity overview section
    render_activity_overview(data=activity_data_df, vars=vars)
