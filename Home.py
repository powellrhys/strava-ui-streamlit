import streamlit as st

from functions.ui_components import \
    configure_page_config, \
    homepage_metrics

from functions.collect_data import \
    read_activity_data

from functions.variables import \
    Variables

# Setup page config
configure_page_config()

# Collect codebase variables
vars = Variables

# Read in activity data
activity_data = read_activity_data()

# Define page title and header
st.title('STRAVA DASHBOARD')
st.header(f'Yearly distance stats to date ({vars.current_year})')

# Render homepage metrics ui component
homepage_metrics(activity_data=activity_data,
                 vars=vars)
