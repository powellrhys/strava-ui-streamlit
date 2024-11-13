import streamlit as st
import plotly.express as px
from datetime import datetime

from functions.ui_components import \
    configure_page_config

from functions.collect_data import \
    read_activity_data

# Setup page config
configure_page_config()

# Read in activity data
activity_data = read_activity_data()

# Convert distance from meters to kilometers
activity_data['distance'] = activity_data['distance'] / 1000

# Collect a list of unique activity types
all_activity_types = activity_data['type'].unique().tolist()

st.title('Progress')
# Define the range for the slider
start_date = datetime(2016, 1, 1)
end_date = datetime(datetime.now().year, 12, 31)

# Create a slider with two datetime values
date_range = st.sidebar.slider(
    label="Select a range of dates:",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format="MM/YYYY"
)

# Activity multiselect input
selected_activity_type = st.sidebar.multiselect(label='Activity Type',
                                                options=all_activity_types,
                                                default=['Run'])

# Metric select box
metric = st.sidebar.selectbox(label='Metric',
                              options=['Distance',
                                       'Count',
                                       'Kudos Count',
                                       'Total Elevation Gain',
                                       'Moving Time'])

# Chart type radio input
chart_type = st.sidebar.radio(label='Plot Type',
                              options=['Bar', 'Line'])

# Granularity radio input
plot_resolution = st.sidebar.radio(label='Plot Resolution',
                                   options=['Yearly', 'Monthly'])

# Map granularity input to chart resolution
if plot_resolution == 'Yearly':
    resolution = 'Y'
elif plot_resolution == 'Monthly':
    resolution = 'M'

if metric == 'Count':
    grouped_df = activity_data \
        .groupby([activity_data['start_date'].dt.to_period(resolution), 'type'])['type'] \
        .count().reset_index(name='count')

# Aggregate data by distance
else:
    grouped_df = activity_data \
        .groupby([activity_data['start_date'].dt.to_period(resolution), 'type']) \
        .sum().reset_index()

# Filter by activity type
grouped_df = grouped_df[grouped_df['type'].isin(selected_activity_type)]

# Convert 'date' back to datetime for plotting purposes
grouped_df['start_date'] = grouped_df['start_date'].dt.to_timestamp()

# Filter by date range
grouped_df = grouped_df[(grouped_df['start_date'] >= date_range[0]) & (grouped_df['start_date'] <= date_range[1])]

# Define figure attributes
chart_func = getattr(px, chart_type.lower())

# Generate figure
fig = chart_func(grouped_df,
                 x='start_date',
                 y=metric.lower().replace(' ', '_'),
                 color='type',
                 labels={'start_date': 'Date',
                         'type': 'Activity Type',
                         metric.lower().replace(' ', '_'): metric},
                 title=f'{plot_resolution} {metric} by Type')

# Illustrate figure
st.plotly_chart(fig)
