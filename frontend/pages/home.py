# Import python dependencies
import streamlit as st

# Import project dependencies
from streamlit_components.ui_components import (
    configure_page_config,
    data_source_badge
)
from functions.data_functions import (
    StravaData,
    Variables
)
from functions.ui_components import \
    homepage_metrics

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

    # Define page title and header
    st.title('STRAVA DASHBOARD')
    st.header(f'Yearly distance stats to date ({vars.current_year})')

    activity_data_df = StravaData(blob_connection_string=vars.blob_connection_string,
                                  container_name='strava',
                                  blob_name='activity_data.csv')

    # Render homepage metrics ui component
    homepage_metrics(activity_data=activity_data_df.return_dataframe(),
                     vars=vars)

    # Render data source metadata badge
    data_source_badge(blob_connection_string=vars.blob_connection_string,
                      container_name='strava',
                      file_name='activity_data.csv')
