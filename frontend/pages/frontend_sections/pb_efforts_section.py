# Import dependencies
from functions.data_functions import StravaData, Variables, read_json_from_blob, seconds_to_mmss
from streamlit_components.plot_functions import PlotlyPlotter
import streamlit as st
import pandas as pd
import numpy as np

def render_running_pb_section(data: StravaData, vars: Variables) -> None:
    """
    Simple streamlit section to render best PB efforts for various distances
    """
    # Render page title
    st.title("Running PB Effort Overview")

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
        # Define columns to store user inputs
        columns = st.columns([3, 2])

        # Render pb effort progress plot within first column
        with columns[0]:
            with st.container(border=True):
                fig = PlotlyPlotter(
                    df,
                    x="date",
                    y="minutes",
                    markers=True,
                    title=f"Overview of PB efforts for {distance_map[distance]}",
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

        # Render pb effort leaderboard in final column container
        with columns[-1]:
            with st.container(border=True):
                df = df.sort_values("minutes").reset_index()
                leaderboard_df = df[["name", "time", "date"]]
                leaderboard_df = leaderboard_df.rename(
                    columns={"name": "Activity Name", "time": "Time", "date": "Date"})

                st.dataframe(leaderboard_df, hide_index=True)

        # Collect activity names for specific distance
        efforts = df[df['name'].str.contains(distance_map[distance], na=False)]["name"]

        # Define 3 column objects
        columns = st.columns([6, 1, 1])

        # Render multiselect object within first column
        with columns[0]:
            activities = st.multiselect(label="Activities To Analysis", options=efforts)

        # Render plot metric pills within final column
        with columns[-1]:
            plot_metric = st.pills(label="Plot Breakdown", options=["Splits", "Raw"], default="Splits")

        # Filter effort data by selected activities
        effort_df = df[df["name"].isin(activities)]

        # If activities have been selected, render the following section
        if len(effort_df) > 0:

            # Create activity name and index dictionary to collect data from blob
            activities = effort_df.set_index("name")["id"].to_dict()

            # Define empty dataframe and iterate through selected activities
            all_effort_df = pd.DataFrame()
            for activity_name, activity_id in activities.items():

                # Read activity stream from blob
                data = read_json_from_blob(vars=vars,
                                           container_name="strava",
                                           blob_name=f"stream/{activity_id}.json")

                # Fetch data of interest and write to a dataframe + append activity name column
                single_effort_df = pd.DataFrame(data[plot_metric.lower()])
                single_effort_df["Activity Name"] = activity_name

                # Concat activity data to all effort dataframe
                all_effort_df = pd.concat([all_effort_df, single_effort_df], ignore_index=True)

            # If plot metric is splits, create splits string for plot
            if plot_metric == "Splits":
                all_effort_df["split_str"] = (
                    all_effort_df["split_time"]
                    .astype(int)
                    .apply(lambda s: f"{s // 60}:{s % 60:02d}")
                )

            # If plot metric is raw, create pace and time columns ready for plot
            else:
                # Convert velocity (m/s) to pace in seconds per km
                all_effort_df['pace_sec'] = 1000 / all_effort_df['velocity_smooth']
                all_effort_df["distance"] = all_effort_df["distance"] / 1000

                # Calculate data point pace
                all_effort_df['pace'] = all_effort_df['velocity_smooth'].apply(
                    lambda x: f"{int((1000/x)//60)}:{int(round((1000/x) % 60)):02d}" if x > 0 else "Invalid speed"
                )

            # Define plot config for both plot types
            plot_dict = {
                "Splits": {
                    "x": "split_number",
                    "y": "split_time",
                    "hover_data": {"split_str": True, "split_time": False},
                    "labels": {
                        "split_number": "Distance (km)",
                        "split_time": "Split Time (sec)",
                        "split_str": "Splits (mm:ss/km)"
                    }
                },
                "Raw": {
                    "x": "distance",
                    "y": "pace_sec",
                    "hover_data": {"pace": True, "pace_sec": False, "distance": ":.2f"},
                    "labels": {
                        "distance": "Distance (km)",
                        "pace_sec": "Split Time (sec)",
                        "pace": "Split (mm:ss/km)"
                    }
                }
            }

            # Generate plot using plot config outlined above
            fig = PlotlyPlotter(
                all_effort_df,
                x=plot_dict[plot_metric]["x"],
                y=plot_dict[plot_metric]["y"],
                color="Activity Name",
                markers=True,
                title=f"{distance} Pace Breakdown",
                hover_data=plot_dict[plot_metric]["hover_data"],
                labels=plot_dict[plot_metric]["labels"],
            ).plot_line()

            # Define axis mapping config dictionary to handle both plot types
            axis_mapping = {"Splits": "split_time", "Raw": "pace_sec"}

            # Collect Min and max of splits
            min_sec = all_effort_df[axis_mapping[plot_metric]].min()
            max_sec = all_effort_df[axis_mapping[plot_metric]].max()

            # Generate 6 evenly spaced ticks and values
            tickvals = np.linspace(min_sec, max_sec, 6)
            ticktext = [seconds_to_mmss(s) for s in tickvals]

            # Update ya
            fig.update_yaxes(
                tickvals=tickvals,
                ticktext=ticktext,
                autorange="reversed",
                title_text="Splits (mm:ss/km)"
            )

            # Render plot within container
            with st.container(border=True):
                st.plotly_chart(fig)

        # Render message on screen if no activities were selected
        else:
            st.info("No activities selected for analysis")

    # Render message on screen if no records have been recorded for specific distance
    else:
        st.info(f"No effort data recorded for {distance_map[distance]}")
