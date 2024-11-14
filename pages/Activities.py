import streamlit as st
from datetime import datetime
import pandas as pd

from functions.ui_components import \
    configure_page_config

from functions.collect_data import \
    read_activity_data

# Setup page config
configure_page_config()

start_date = datetime(2016, 1, 1)
end_date = datetime(datetime.now().year, 12, 31)

# Read in activity data
activity_data = read_activity_data()
activity_data = activity_data.drop([activity_data.columns[0]], axis=1)

# Collect a list of unique activity types
all_activity_types = activity_data['type'].unique().tolist()

st.title('Activity Overview')

# Create a slider with two datetime values
date_range = st.sidebar.slider(
    label="Select a range of dates:",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format="MM/YYYY"
)

selected_activity_types = st.sidebar \
    .multiselect(label='Activity',
                 options=all_activity_types,
                 default=['Run'])

activity_data = activity_data[activity_data['type'].isin(selected_activity_types)]

# # Convert 'date' back to datetime for plotting purposes
# activity_data['start_date'] = activity_data['start_date'].dt.to_timestamp()

for column in activity_data.columns:
    activity_data = activity_data \
        .rename(columns={
            column: column.replace('_', ' ').upper()
        })

activity_data['DATE'] = pd.to_datetime(activity_data['START DATE']).dt.date

activity_data = activity_data[['NAME',
                               'DISTANCE',
                               'MOVING TIME',
                               'TOTAL ELEVATION GAIN',
                               'TYPE',
                               'DATE',
                               'KUDOS COUNT'
                               ]]

st.dataframe(data=activity_data,
             use_container_width=True,
             hide_index=True)
