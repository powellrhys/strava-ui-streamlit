# Import dependencies
from streamlit_components.plot_functions import PlotlyPlotter
from functions.data_functions import StravaData, Variables, read_json_from_blob
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

        columns = st.columns([3, 2])

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

        with columns[-1]:
            with st.container(border=True):
                df = df.sort_values("minutes").reset_index()
                leaderboard_df = df[["name", "time", "date"]]
                leaderboard_df = leaderboard_df.rename(
                    columns={"name": "Activity Name", "time": "Time", "date": "Date"})

                st.dataframe(leaderboard_df, hide_index=True)

        efforts = df[df['name'].str.contains(distance_map[distance], na=False)]["name"]

        columns = st.columns([6, 1, 1])

        with columns[0]:
            activities = st.multiselect(label="Activities To Analysis", options=efforts)

        with columns[-1]:
            plot_metric = st.pills(label="Plot Breakdown", options=["Splits", "Raw"], default="Splits")

        effort_df = df[df["name"].isin(activities)]

        if len(effort_df) > 0:

            activities = effort_df.set_index("name")["id"].to_dict()

            all_effort_df = pd.DataFrame()
            for activity_name, activity_id in activities.items():

                data = read_json_from_blob(vars=vars,
                                           container_name="strava",
                                           blob_name=f"stream/{activity_id}.json")

                single_effort_df = pd.DataFrame(data[plot_metric.lower()])
                single_effort_df["Activity Name"] = activity_name

                all_effort_df = pd.concat([all_effort_df, single_effort_df], ignore_index=True)

            if plot_metric == "Splits":
                all_effort_df["split_str"] = (
                    all_effort_df["split_time"]
                    .astype(int)
                    .apply(lambda s: f"{s // 60}:{s % 60:02d}")
                )

            else:

                # Convert velocity (m/s) to pace in seconds per km
                all_effort_df['pace_sec'] = 1000 / all_effort_df['velocity_smooth']  # seconds per km
                all_effort_df["distance"] = all_effort_df["distance"] / 1000

                all_effort_df['pace'] = all_effort_df['velocity_smooth'].apply(
                    lambda x: f"{int((1000/x)//60)}:{int(round((1000/x) % 60)):02d}" if x > 0 else "Invalid speed"
                )

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

            fig = PlotlyPlotter(
                all_effort_df,
                x=plot_dict[plot_metric]["x"],
                y=plot_dict[plot_metric]["y"],
                color="Activity Name",
                markers=True,
                title=f"{distance_map[distance]} Breakdown",
                hover_data=plot_dict[plot_metric]["hover_data"],
                labels=plot_dict[plot_metric]["labels"],
            ).plot_line()

            if plot_metric == "Splits":

                # Min and max of splits
                min_sec = all_effort_df["split_time"].min()
                max_sec = all_effort_df["split_time"].max()

                # Generate 6 evenly spaced ticks
                tickvals = np.linspace(min_sec, max_sec, 6)

                # Convert back to mm:ss
                def seconds_to_mmss(seconds):
                    minutes = int(seconds // 60)
                    sec = int(seconds % 60)
                    return f"{minutes:02d}:{sec:02d}"

                ticktext = [seconds_to_mmss(s) for s in tickvals]

                fig.update_yaxes(
                    tickvals=tickvals,
                    ticktext=ticktext
                )

            else:
                # Function to convert seconds to mm:ss
                def seconds_to_mmss(seconds):
                    minutes = int(seconds // 60)
                    sec = int(seconds % 60)
                    return f"{minutes:02d}:{sec:02d}"

                # Determine min and max pace for y-axis
                min_sec = all_effort_df["pace_sec"].min()
                max_sec = all_effort_df["pace_sec"].max()

                # Generate 6 evenly spaced ticks
                tickvals = np.linspace(min_sec, max_sec, 6)
                ticktext = [seconds_to_mmss(s) for s in tickvals]

                # Update y-axis to show mm:ss
                fig.update_yaxes(
                    tickvals=tickvals,
                    ticktext=ticktext,
                    title="Split Time (mm:ss)"
                )

            fig.update_yaxes(autorange="reversed")
            fig.update_yaxes(title_text="Splits (mm:ss/km)")
            st.plotly_chart(fig)

        else:
            st.info("No activities selected for analysis")

    else:
        st.info(f"No effort data recorded for {distance_map[distance]}")
