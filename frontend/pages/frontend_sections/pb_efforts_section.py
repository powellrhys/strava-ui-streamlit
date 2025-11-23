# Import dependencies
from streamlit_components.plot_functions import PlotlyPlotter
from functions.data_functions import StravaData
import streamlit as st
import pandas as pd

def render_running_pb_section(data: StravaData) -> None:
    """
    """
    # Render distance selectbox
    distance = st.selectbox(label="Distance", options=["5km", "10km", "Half Marathon"], index=2)

    # Filter dataframe based on user selected option
    distance_map = {"5km": "5km", "10km": "10km", "Half Marathon": "HM"}
    df = data.return_dataframe()
    df = df[df["name"].str.contains(distance_map[distance])]

    # Convert columns
    df["date"] = pd.to_datetime(df["start_date"])
    df["time_delta"] = pd.to_timedelta(df["time"])
    df["minutes"] = df["time_delta"].dt.total_seconds() / 60

    # Render plot of pb efforts over time
    if len(df) > 0:
        with st.container(border=True):
            fig = PlotlyPlotter(
                df,
                x="date",
                y="minutes",
                markers=True,
                title="Race Times Over Dates",
                hover_name="name",
                labels={
                    "minutes": "Minutes",
                    "date": "Date",
                    "time": "Time"
                },
                text="time",
                hover_data={
                    "time": True,
                    "minutes": False,
                    "date": True,
                    "name": False
                }
            ).plot_line()

            # Update plot config
            fig.update_traces(textposition="top center", textfont=dict(size=12))
            fig.update_traces(line=dict(color="#fc4c02"))

            # Render plot
            st.plotly_chart(fig)

    else:
        st.info(f"No PB efforts recorded for {distance}")
