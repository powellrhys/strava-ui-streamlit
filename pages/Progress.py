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
all_activity_types = activity_data['type'].unique().tolist()

st.title('Progress')
# Define the range for the slider
start_date = datetime(2016, 1, 1)
end_date = datetime(datetime.now().year, 12, 31)

# Create a slider with two datetime values
date_range = st.sidebar.slider(
    "Select a range of dates:",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format="MM/YYYY"
)

selected_activity_type = st.sidebar.multiselect(label='Activity Type',
                                                options=all_activity_types,
                                                default=['Run'])

chart_type = st.sidebar.radio(label='Plot Type',
                              options=['Bar', 'Line'])

plot_resolution = st.sidebar.radio(label='Plot Resolution',
                                   options=['Yearly', 'Monthly'])

if plot_resolution == 'Yearly':
    resolution = 'Y'
elif plot_resolution == 'Monthly':
    resolution = 'M'

grouped_df = activity_data.groupby([activity_data['start_date'].dt.to_period(resolution), 'type']).sum().reset_index()

grouped_df = grouped_df[grouped_df['type'].isin(selected_activity_type)]

# Convert 'date' back to datetime for plotting purposes
grouped_df['start_date'] = grouped_df['start_date'].dt.to_timestamp()

grouped_df = grouped_df[(grouped_df['start_date'] >= date_range[0]) & (grouped_df['start_date'] <= date_range[1])]

# Plotting using Plotly Express
fi = chart_func = getattr(px, chart_type.lower())

fig = chart_func(grouped_df, x='start_date', y='distance', color='type',
                 labels={'start_date': 'Year', 'distance': 'Total Distance'},
                 title='Yearly Total Distance by Type')

st.plotly_chart(fig)
