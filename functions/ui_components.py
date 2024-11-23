# Import python dependencies
import streamlit as st
import pandas as pd
import warnings
import time

# Import project functions
from functions.github_actions import \
    monitor_github_action
from functions.variables import \
    Variables


def configure_page_config(initial_sidebar_state: str = "expanded",
                          layout: str = "wide") -> None:
    '''
    Input: Page config parameters
    Output: None
    Function to define page config
    '''
    # Set page config
    st.set_page_config(
        initial_sidebar_state=initial_sidebar_state,
        layout=layout,
        page_icon=':running_shirt_with_sash:'
    )

    # Ignore all warnings
    warnings.filterwarnings("ignore")

    if 'activity_data' not in st.session_state:
        st.session_state['logged_in'] = False


def login_page() -> None:

    # Collect project variables
    vars = Variables()

    # Login page title
    st.title('Login Page')

    # Define column structure for page
    col1, _ = st.columns([2, 3])

    with col1:

        # Collect user login inputs
        username = st.text_input(label='Username')
        password = st.text_input(label='Password',
                                 type='password')

        # Compare user inputs with accepted values
        if username == vars.app_username and password == vars.app_password:

            # If credentials are correct
            st.session_state['logged_in'] = True

            # Reload page
            st.rerun()

        else:
            # Display error message
            st.warning('Username/Password invalid')


def homepage_metrics(activity_data: pd.DataFrame,
                     vars: Variables) -> None:
    '''
    Input: Activity data and variables object
    Output: Homepage metrics component
    Function to generate homepage mentrics component
    '''
    # Define activity types of interest
    activity_types = ['Run', 'Ride', 'Swim', 'Golf', 'Walk']

    # Iterate through all activity types to get the previous 2 years of data
    data = {}
    for type in activity_types:

        # Collect yearly data
        yearly_data = {}
        for year in [vars.current_year, vars.previous_year]:

            filtered_df = activity_data[(activity_data['type'] == type) & (activity_data['start_date'].dt.year == year)]

            yearly_data[year] = {
                'entries': len(filtered_df),
                'distance': filtered_df['distance'].sum()/1000
            }

            # Append yearly data to dictionary
            data[type] = yearly_data

    # Define columns
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    # Iterate through columns to create metric components
    for i in range(len(columns)):

        # Calculate the difference in distance between this year and last year
        diff = data[activity_types[i]][vars.current_year]['distance'] - \
            data[activity_types[i]][vars.previous_year]['distance']

        # Render metric components
        with columns[i]:
            st.metric(label=activity_types[i],
                      value=f"{round(data[activity_types[i]][2024]['distance'], 2)} km",
                      delta=f"{round(diff, 2)} km"
                      )


def github_actions_alerts(access_token: str,
                          workflow_run_id: str,
                          poll_interval: int = 10) -> None:
    '''
    Input: GitHub access toke, github action workflow id, polling frequency
    Output: None
    Function to display github action alerts on the frontend
    '''
    # Define empty streamlit container
    with st.empty():

        # Define counter variable
        counter = 1

        # Continue to poll github action until action is complete
        while True:

            # Get status of github action
            response = monitor_github_action(access_token=access_token,
                                             workflow_run_id=workflow_run_id)

            # Handle request error
            if response.status_code != 200:
                st.error(f"Error fetching workflow run status: {response.status_code} {response.text}")
                return None

            # Decode response
            run_data = response.json()
            status = run_data.get("status")
            conclusion = run_data.get("conclusion")

            # Handle successful request
            if status == "completed":
                st.success(f"Workflow completed with conclusion: {conclusion}")
                return None
            else:
                st.info(f"Pipeline Status Checks Made: {counter} - Workflow Run Status: {status}")

            # Delay next request
            time.sleep(poll_interval)

            # Increment counter variable
            counter = counter + 1
