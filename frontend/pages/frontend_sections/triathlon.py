# Import dependencies
from streamlit_components.plot_functions import PlotlyPlotter
from functions.data_functions import StravaData, Variables
from dateutil.relativedelta import relativedelta
import streamlit as st
import pandas as pd

def render_running_pb_section(data: StravaData, vars: Variables) -> None:
    """
    """
    # Render page title
    st.title("Triathlon Training Overview")

    # Define sport mapping dictionary
    sport_map = {"Running": "Run", "Cycling": "Ride", "Swimming": "Swim"}

    # Define input widget columns
    columns = st.columns([1, 3, 1])

    # Render date range slide bar in first column
    with columns[0]:
        date_range = st.slider(
            label="Select a range of dates:",
            min_value=vars.current_date - relativedelta(months=24),
            max_value=vars.current_date,
            value=(vars.current_date - relativedelta(months=6), vars.current_date),
            format="MM/YYYY"
        )

    # Render metric pills within final column
    with columns[-1]:
        metric = st.pills(label="Metric", options=["Total Distance", "Activity Count"], default="Total Distance")

    # Filter data by selected date range
    data.filter_data_by_date_range(min_date=date_range[0],
                                   max_date=date_range[1],
                                   column_name='start_date')

    # Return dataframe object and perform transformations ready for processing
    df = data.return_dataframe()
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["week"] = df["start_date"].dt.to_period("W").apply(lambda r: r.start_time)

    # Define sport columns and iterate through each column
    columns = st.columns(3)
    for i, sport in enumerate(["Running", "Cycling", "Swimming"], start=0):

        # Within the first column, render a container object
        with columns[i]:
            with st.container(border=True):

                # Filter data to include column sport
                sport_df = df[df["type"].str.contains(sport_map[sport], na=False)]

                # Aggregate data by week
                weekly_summary = (sport_df.groupby("week").agg(
                    total_distance=("distance", "sum"), activity_count=("distance", "count")))

                # Ensure all weeks are present
                all_weeks = pd.date_range(start=df["week"].min(), end=df["week"].max(), freq="W-MON")
                weekly_summary = (weekly_summary.reindex(all_weeks, fill_value=0).rename_axis("week").reset_index())

                # Convert meters → km and ensure activity count is an integer
                weekly_summary["total_distance"] /= 1000
                weekly_summary["activity_count"] = weekly_summary["activity_count"].astype(int)

                # Generate plotly express bar plot
                fig = PlotlyPlotter(
                    weekly_summary,
                    x="week",
                    y=metric.lower().replace(" ", "_"),
                    color_discrete_sequence=["#fc4c02"],
                    title=f"{sport} - Weekly {metric} Over Time",
                    labels={
                        "week": "Week",
                        "total_distance": "Distance (km)",
                        "activity_count": "Activity Count"
                    },
                ).plot_bar()

                # Update bar plot figure
                fig.update_layout(
                    xaxis_tickformat="%Y-%m-%d",
                    hovermode="x unified",
                )

                # Render bar plot with column container
                st.plotly_chart(fig, use_container_width=True)
