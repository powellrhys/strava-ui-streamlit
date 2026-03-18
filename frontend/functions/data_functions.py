# Import python dependencies
from streamlit_components.data_functions import BlobData
from azure.storage.blob import BlobServiceClient
from folium.plugins import TimestampedGeoJson
from folium.plugins import Fullscreen
from typing import Tuple
import streamlit as st
import datetime as dt
import pandas as pd
import polyline
import folium
import json

class Variables:
    """
    Loads configuration and environment variables from the `.streamlit/secrets.toml` file.

    This class centralizes access to important constants such as date parameters and
    sensitive credentials like the Azure Blob Storage connection string.

    Attributes:
        current_year (int): The current calendar year.
        previous_year (int): The previous calendar year.
        first_activity_date (datetime): The fixed start date for activities (January 1, 2016).
        end_of_current_year (datetime): The end of the current year (December 31).
        current_date (datetime): The current date and time.
        blob_connection_string (str): Azure Blob Storage connection string loaded from secrets.
    """
    def __init__(self):

        # Date related variables
        self.current_year = dt.date.today().year
        self.previous_year = dt.date.today().year - 1
        self.first_activity_date = dt.datetime(2016, 1, 1)
        self.current_date = dt.datetime.now()
        self.end_of_current_year = dt.datetime(dt.datetime.now().year, 12, 31)

        # Collect environmental variables
        self.blob_connection_string = st.secrets['general']['blob_connection_string']

class StravaData(BlobData):
    """
    A subclass of BlobData tailored for handling Strava-specific data operations.

    This class can be extended to include methods and properties
    specific to fetching, processing, and managing Strava activity data.
    """
    def filter_data_by_date_range(
        self,
        min_date: str,
        max_date: str,
        column_name: str
    ) -> None:
        """
        Filters the DataFrame in-place to include only rows where the specified date column
        falls within the given date range.

        Converts the `min_date` and `max_date` parameters, as well as the target column,
        to datetime objects (removing any timezone information) before applying the filter.

        Args:
            min_date (str): The start date (inclusive) of the filter range, in a format parsable by pandas.
            max_date (str): The end date (inclusive) of the filter range, in a format parsable by pandas.
            column_name (str): The name of the date column in the DataFrame to filter on.

        Returns:
            None: The filtering is done in-place, modifying `self.df`.
        """
        min_date = pd.to_datetime(min_date)
        max_date = pd.to_datetime(max_date)

        self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce').dt.tz_localize(None)
        self.df = self.df[
            (self.df[column_name] >= min_date) & (self.df[column_name] <= max_date)]

    def filter_column_by_list(
        self,
        column_name: str,
        filter_values: list
    ) -> None:
        """
        Filters the DataFrame in-place to include only rows where the specified column's values
        are present in the given list of filter values.

        Args:
            column_name (str): The name of the column to filter.
            filter_values (list): A list of values to keep in the column.

        Returns:
            None: The filtering modifies `self.df` in-place.
        """
        self.df = self.df[self.df[column_name].isin(filter_values)]

    def convert_distance_into_km(
        self,
        column_name: str = 'distance'
    ) -> None:
        """
        Converts distance values in the specified column from meters to kilometers,
        rounding to two decimal places.

        Args:
            column_name (str): The name of the distance column to convert. Defaults to 'distance'.

        Returns:
            None: The conversion is applied in-place to `self.df`.
        """
        self.df[column_name] = (self.df[column_name] / 1000).round(2)

    def calculate_moving_time(
        self,
        column_name: str = 'moving_time'
    ) -> None:
        """
        Converts moving time values from seconds into a formatted string "H:MM".

        Args:
            column_name (str): The name of the column containing moving time in seconds.
                            Defaults to 'moving_time'.

        Returns:
            None: The conversion is applied in-place to `self.df`.
        """
        self.df[column_name] = self.df[column_name] \
            .apply(lambda x: f"{x // 3600}:{(x % 3600) // 60:02}")

    def map_column_header(
        self,
        mapping_dict: dict
    ) -> None:
        """
        Renames columns in the DataFrame according to the provided mapping dictionary,
        and reorders the DataFrame to include only the renamed columns.

        Args:
            mapping_dict (dict): A dictionary where keys are current column names and values are new column names.

        Returns:
            None: The DataFrame `self.df` is modified in-place.
        """
        # Rename and select dataframe columns
        self.df = self.df.rename(columns=mapping_dict)
        self.df = self.df[list(mapping_dict.values())]

def generate_heatmap(
    data: StravaData
) -> None:
    """
    Generates an interactive folium heatmap of Strava activity routes and updates
    the Streamlit session state with the map HTML for display and download.

    The function decodes GPS polylines from Strava activity data and plots them on
    a map centered around a fixed location. Activities with zero distance or invalid
    data are ignored. Fullscreen control is added to the map.

    Args:
        data (StravaData): An instance containing Strava activity data with decoded polylines.

    Side Effects:
        - Writes the generated map HTML to `st.session_state.buffer`.
        - Enables the download button by setting `st.session_state.download_disabled` to False.
    """
    # Construct folium object
    m = folium.Map(tiles='cartodb positron', location=[51.4837, 0], zoom_start=6)

    # Iterate through activity data and collect polylines
    for _, row in data.return_dataframe().iterrows():

        try:
            # Filter out activities with no gps data
            if row['distance'] > 0:

                # Collect polyline data
                curve = row['map']

                # Decode polyline data
                data = polyline.decode(curve)

                # Add polyline data to folium object
                folium.PolyLine(data,
                                color='#fc4c02',
                                weight=1,
                                opacity=0.7).add_to(m)

        except BaseException:
            pass

    # Add full screen functionality to folium object
    Fullscreen(position="topleft").add_to(m)

    # Convert to html format
    map_html = m._repr_html_()

    # Update buffer variable with folium object
    st.session_state.buffer.write(map_html.encode())
    st.session_state.buffer.seek(0)

    # Make download available
    st.session_state.download_disabled = False

def generate_coastal_path_heatmap(
    vars: Variables
) -> folium.Map._repr_html_:
    """
    Generates an interactive Folium heatmap of Strava activities along the coastal path.

    This function:
    - Converts the provided StravaData object into a list of activity records
    - Initializes a Folium map centered on Wales
    - Plots each activity's GPS polyline onto the map with a tooltip of its name
    - Enables fullscreen map functionality
    - Returns the HTML representation of the rendered map

    Parameters:
    ----------
    data : StravaData
        An object that provides access to Strava activity data, including encoded polylines.

    Returns:
    -------
    folium.Map._repr_html_
        An HTML string representing the rendered heatmap for embedding or display.
    """
    # Convert dataframe into list of dictionaries
    activity_data = StravaData(blob_connection_string=vars.blob_connection_string,
                               container_name='strava',
                               blob_name='wcp_segments.csv').return_dataframe().to_dict(orient='records')

    # activity_data = data.return_dataframe().

    # Generate folium map object
    m = folium.Map(tiles='cartodb positron',
                   location=[52.4837, -3.5],
                   zoom_start=7)

    # Iterate through activities
    for activity in activity_data:

        # Collect and decode activity polyline
        curve = activity["polyline"]
        data = polyline.decode(curve)

        # Plot gps data on map object
        folium.PolyLine(data,
                        color='#fc4c02',
                        weight=2,
                        opacity=1,
                        tooltip=activity['name']).add_to(m)

    # Add full screen functionality to folium object
    Fullscreen(position="topleft").add_to(m)

    # Convert to html format
    map_html = m._repr_html_()

    return map_html

def sum_coastal_path_distance(data: StravaData) -> Tuple[float, pd.DataFrame]:
    """
    Extract and sum Welsh Coastal Path (WCP) distances from Strava activity data.

    Looks for patterns like "[WCP - X]" in activity names, where X is a distance value.
    Returns the total distance and a yearly summary based on activity start dates.

    Parameters
    ----------
    data : StravaData
        A StravaData object with 'name' and 'start_date' fields.

    Returns
    -------
    total_distance : float
        Total summed WCP distance.
    distance_per_year : pandas.DataFrame
        Yearly totals of WCP distance.
    """
    # Return dataframe from StravaData object
    df = data.return_dataframe()

    # Use regex to extract the number after 'WCP - ' and before ']'
    df['wcp_value'] = df['name'].str.extract(r'\[WCP\s*-\s*([\d.]+)\]', expand=False)

    # Convert to numeric (in case some are NaN or strings)
    df['wcp_value'] = pd.to_numeric(df['wcp_value'], errors='coerce')

    # Make sure start_date is a datetime
    df['start_date'] = pd.to_datetime(df['start_date'])

    # Extract the year from the start date
    df['year'] = df['start_date'].dt.year

    # Group by year and sum the distance
    distance_per_year = df.groupby('year')['wcp_value'].sum().reset_index()

    return float(df['wcp_value'].sum()), distance_per_year

def read_json_from_blob(vars: Variables, container_name: str, blob_name: str) -> list:
    """
    Read and parse a JSON blob from Azure Blob Storage.

    Args:
        vars (Variables): Config object containing the blob connection string.
        container_name (str): Name of the blob container.
        blob_name (str): Name of the JSON blob.

    Returns:
        list: Parsed JSON content.
    """
    # Connect to Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(
        vars.blob_connection_string
    )

    # Define blob container client
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    # Download and parse JSON
    downloaded_bytes = blob_client.download_blob().readall()
    data = json.loads(downloaded_bytes)

    return data

def seconds_to_mmss(seconds):
    """
    Convert seconds to a MM:SS formatted string.

    Args:
        seconds (float | int): Duration in seconds.

    Returns:
        str: Time formatted as minutes and seconds (MM:SS).
    """
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

@st.cache_data
def load_and_cache_data(blob_connection_string: str, container_name: str, blob_name: str) -> pd.DataFrame:
    """
    Load data from Azure Blob Storage and return as a DataFrame.
    """
    # Download welsh peak data from blob storage account
    welsh_peaks_df = StravaData(blob_connection_string=blob_connection_string,
                                container_name=container_name,
                                blob_name=blob_name)

    return welsh_peaks_df.return_dataframe()

@st.cache_data
def build_mountain_map(df_json: dict, min_height: int, counties: list) -> folium.Map:
    """
    Build a folium map of Welsh mountains based on the provided data and filters.
    """
    # Load data and apply filters
    df = pd.read_json(df_json)
    df = df[df["Feet"] >= min_height]

    # Filter by county if any are selected
    if counties:
        df = df[df["County"].isin(counties)]

    if df.empty:
        return None

    # Create map centered on the average location of the mountains
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()])
    m.fit_bounds([[df["Latitude"].min(), df["Longitude"].min()], [df["Latitude"].max(), df["Longitude"].max()]])
    Fullscreen().add_to(m)

    # Add markers for each mountain
    for _, row in df.iterrows():
        color = "green" if row["climbed"] is True else "red"
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                f"<b>{row['Name']}</b><br>"
                f"Height: {row['Metres']}m / {row['Feet']}ft<br>"
                f"County: {row['County']}<br>"
                f"Climbed: {'✅' if row['climbed'] else '❌'}",
                max_width=200,
            ),
            tooltip=row["Name"],
            icon=folium.Icon(color=color, icon="mountain", prefix="fa"),
        ).add_to(m)

    return m

def seconds_to_timestamp(seconds: int) -> str:
    """
    Convert seconds to a timestamp string in the format
    """
    # Assuming the base date is arbitrary since we only care about the time component
    h = seconds // 3600
    mins = (seconds % 3600) // 60
    s = seconds % 60

    return f"2024-01-01T{h:02d}:{mins:02d}:{s:02d}"


def create_route_animation(ids: list[str], vars: Variables) -> folium.Map:
    """
    """
    # Define a list of colours to cycle through for different routes
    COLOURS = [
        "#00FFFF", "#FF69B4", "#DA70D6", "#FF8C00", "#FF1493",
        "#00FF00", "#FFD700", "#32CD32", "#FF4500", "#1E90FF"
        ]

    # Collect all coordinates from the selected activities to calculate average location for map centering
    all_coords = []
    route_datasets = []

    # Iterate through selected activities and collect coordinate data from blob
    for id in ids:

        # Read activity stream from blob
        data = read_json_from_blob(vars=vars,
                                   container_name="strava",
                                   blob_name=f"stream/{id}.json")

        # Extract coordinates and check if they exist before proceeding
        coords = data.get("coords", [])

        # If no coordinates are found, skip this activity and continue with the next one
        if not coords:
            continue
        
        # Extend the all_coords list with the coordinates from this activity for later averaging
        all_coords.extend(coords)
        route_datasets.append({"coords": coords, "name": id})

    # If no valid coordinate data was found in any of the selected activities, raise an error to inform the user
    if not route_datasets:
        raise ValueError("No valid coordinate data found in any JSON file.")

    # Calculate average latitude and longitude for map centering using all collected coordinates
    avg_lat = sum(c["lat"] for c in all_coords) / len(all_coords)
    avg_lng = sum(c["lng"] for c in all_coords) / len(all_coords)

    # Construct folium map object centered on the average location of all routes
    m = folium.Map(location=[avg_lat, avg_lng], zoom_start=15, tiles="CartoDB dark_matter")

    # Merge all routes into a single FeatureCollection
    all_features = []

    # Iterate through each route
    for idx, route in enumerate(route_datasets):

        # Extract coordinates and assign a colour based on the route index
        coords = route["coords"]
        colour = COLOURS[idx % len(COLOURS)]

        # Minimize the number of points by taking every nth point (e.g., every 5th point) to improve performance
        step = 5
        coords_thinned = coords[::step]

        # Create a GeoJSON feature for each coordinate point with the appropriate styling and timestamp for animation
        for c in coords_thinned:
            all_features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [c["lng"], c["lat"]]
                },
                "properties": {
                    "time": seconds_to_timestamp(c["time"]),
                    "icon": "circle",
                    "iconstyle": {
                        "fillColor": colour,
                        "fillOpacity": 0.9,
                        "stroke": True,
                        "color": "#FFFFFF",
                        "weight": 2,
                        "radius": 8
                    }
                }
            })

    # Create a TimestampedGeoJson layer with the collected features and add it to the map
    TimestampedGeoJson(
        data={"type": "FeatureCollection", "features": all_features},
        period="PT5S",
        duration="PT5S",
        auto_play=False,
        loop=False,
        max_speed=50,
        min_speed=50,
        speed_slider=False,
        transition_time=20,
        loop_button=True,
        date_options="HH:mm:ss",
        time_slider_drag_update=True,
        add_last_point=False
    ).add_to(m)

    # Build legend HTML
    legend_items = "".join([
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="
                width: 14px; height: 14px; border-radius: 50%;
                background-color: {COLOURS[i % len(COLOURS)]};
                border: 2px solid #FFFFFF;
                margin-right: 10px; flex-shrink: 0;">
            </div>
            <span style="font-size: 13px; color: #FFFFFF;">{route["name"]}</span>
        </div>
        """
        for i, route in enumerate(route_datasets)
    ])

    # Add legend to the map using a custom HTML element
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 80px;
        left: 15px;
        z-index: 1000;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 14px 18px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-family: monospace;
        backdrop-filter: blur(4px);
    ">
        <div style="font-size: 12px; color: rgba(255,255,255,0.5);
                    text-transform: uppercase; letter-spacing: 1px;
                    margin-bottom: 10px;">Activities</div>
        {legend_items}
    </div>
    """

    # Add the legend HTML to the folium map
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add full screen functionality to folium object
    Fullscreen(position="topleft").add_to(m)

    # Convert to html format
    map_html = m._repr_html_()

    # Update buffer variable with folium object
    st.session_state.animation_buffer.write(map_html.encode())
    st.session_state.animation_buffer.seek(0)

    # Make download available
    st.session_state.download_animation_disabled = False
