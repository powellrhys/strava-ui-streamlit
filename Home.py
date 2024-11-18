import streamlit as st
import webbrowser
import os

from functions.ui_components import \
    configure_page_config, \
    homepage_metrics, \
    login_page

from functions.collect_data import \
    read_activity_data, \
    read_data_metadata

from functions.authentication import \
    get_authorization_url


from functions.variables import \
    Variables

# Setup page config
configure_page_config()

# Collect codebase variables
vars = Variables()

if 'activity_data' not in st.session_state:
    st.session_state['activity_data'] = None

# Read in activity data
if st.session_state.activity_data is None:
    st.session_state['activity_data'] = read_activity_data()

if not st.session_state['logged_in']:

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
    last_updated = read_data_metadata()['last_updated']
    st.write(f'**Data last updated:** {last_updated}')

    # Update Data Button
    update = st.button('Update Data')

    if update:
        with st.spinner('Collecting Data'):

            # Track state of activity_data file
            original_date = os.path.getmtime('data/activity_data.csv')
            modified_date = original_date

            # Generate auth url and redirect to authentication page
            auth_url = get_authorization_url(CLIENT_ID=vars.client_id,
                                             REDIRECT_URI=vars.redirect_url)
            webbrowser.open(auth_url)

            # Monitor state of activity data file
            while original_date == modified_date:
                modified_date = os.path.getmtime('data/activity_data.csv')

            # Update activity data dataframe
            st.session_state['activity_data'] = read_activity_data()

            # Reload page
            st.rerun()
