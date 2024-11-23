# Import python dependencies
import streamlit as st
import time

# Import project functions
from functions.ui_components import \
    github_actions_alerts, \
    configure_page_config, \
    homepage_metrics, \
    login_page
from functions.github_actions import \
    trigger_update_dat_github_action, \
    get_latest_workflow_run_id
from functions.collect_data import \
    read_activity_data, \
    read_data_metadata
from functions.variables import \
    Variables

# Setup page config
configure_page_config(initial_sidebar_state='collapsed')

# Collect codebase variables
vars = Variables()

if 'activity_data' not in st.session_state:
    st.session_state['activity_data'] = None

# Read in activity data
if st.session_state.activity_data is None:
    st.session_state['activity_data'] = read_activity_data(vars=vars)

if not st.session_state['logged_in'] and vars.login_required:

    # Render login component
    login_page()

else:

    # Define page title and header
    st.title('STRAVA DASHBOARD')
    st.header(f'Yearly distance stats to date ({vars.current_year})')

    # Render homepage metrics ui component
    homepage_metrics(activity_data=st.session_state['activity_data'],
                     vars=vars)

    # Define second page header
    st.header('Status of Data')

    # Write out when data was last updated
    last_updated = read_data_metadata(vars=vars)['last_updated']
    st.write(f'**Data last updated:** {last_updated}')

    # Update Data Button
    update = st.button('Update Data')

    if update:
        with st.spinner('Collecting Data'):

            # Trigger collect data github action
            trigger_update_dat_github_action(access_token=vars.github_access_token)

            # Wait and fetch latest github action workflow run id
            time.sleep(5)
            workflow_run_id = get_latest_workflow_run_id(access_token=vars.github_access_token)

            # Render github action alerts ui component
            github_actions_alerts(access_token=vars.github_access_token,
                                  workflow_run_id=workflow_run_id)

            # Update activity data dataframe
            st.session_state['activity_data'] = read_activity_data(vars=vars)

            # Reload page
            st.rerun()
