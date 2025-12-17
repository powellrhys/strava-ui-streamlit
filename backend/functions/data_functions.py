from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv
from typing import Optional
from io import StringIO
import pandas as pd
import requests
import logging
import json
import os

load_dotenv()

class Variables:
    """
    A container class for storing application-wide constants and configuration variables.

    This class loads necessary values such as API credentials and storage connection strings
    from environment variables during initialization.

    Attributes:
        client_id (str): The Strava client ID, loaded from the 'client_id' environment variable.
        client_secret (str): The Strava client secret, loaded from the 'client_secret' environment variable.
        refresh_token (str): The OAuth refresh token, loaded from the 'refresh_token' environment variable.
        storage_account_connection_string (str): Azure Blob Storage connection string,
            loaded from the 'blob_connection_string' environment variable.
    """
    def __init__(self):

        # API related variables
        self.client_id = os.getenv('client_id')
        self.client_secret = os.getenv('client_secret')
        self.refresh_token = os.getenv('refresh_token')

        # Storage account variables
        self.storage_account_conneciton_string = os.getenv('blob_connection_string')


class ApiService:
    """
    A service class responsible for managing API authentication credentials.

    Stores the client ID, client secret, and refresh token required to authenticate
    requests to the API.
    """
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            refresh_token: str,
            logger: logging.Logger) -> None:
        """
        Initializes the ApiService with the necessary authentication credentials.

        Args:
            client_id (str): The client ID for API authentication.
            client_secret (str): The client secret for API authentication.
            refresh_token (str): The refresh token used to obtain new access tokens.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.logger = logger

    def collect_access_token(self) -> Optional[str]:
        """
        Refreshes and retrieves a new access token from the Strava API using the refresh token.

        Sends a POST request to Strava's OAuth token endpoint with the stored client credentials
        and refresh token, then extracts and stores the new access token.

        Returns:
            Optional[str]: The new access token if the request is successful; otherwise, None.

        Side Effects:
            Sets the instance attribute `self.access_token` with the newly obtained token.
        """
        response = requests.post('https://www.strava.com/api/v3/oauth/token',
                                 data={
                                     'client_id': self.client_id,
                                     'client_secret': self.client_secret,
                                     'grant_type': 'refresh_token',
                                     'refresh_token': self.refresh_token})

        tokens = response.json()
        self.access_token = tokens['access_token']

        return self.access_token, tokens

    def get_activity_data(
            self,
            access_token: Optional[str] = None,
            per_page: int = 200,
            page: int = 1) -> list:
        """
        Retrieves a list of athlete activities from the Strava API.

        Fetches activities for the authenticated user, with optional pagination support.

        Args:
            access_token (Optional[str]): The access token for authorization. If None,
                                        uses the instance's stored access token.
            per_page (int): Number of activities to retrieve per page (default is 200).
            page (int): Page number to retrieve (default is 1).

        Returns:
            list: A list of activity records represented as dictionaries.
        """
        if access_token is None:
            access_token = self.access_token

        # Define activity url
        activities_url = "https://www.strava.com/api/v3/athlete/activities"

        # Define request header and parameters
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': per_page, 'page': page}

        # Execute request
        data = requests.get(
            url=activities_url,
            headers=header,
            params=param
        ).json()

        return data

    def collect_all_activity_data(
            self,
            access_token: Optional[str] = None,
            per_page: int = 200) -> list:
        """
        Retrieves all athlete activity data from the Strava API by paginating through results.

        This method continuously fetches activity data page by page until no more activities
        are returned, aggregating all results into a single list.

        Args:
            access_token (Optional[str]): The access token for API authorization. If None,
                                        the instance's stored access token will be used.
            per_page (int): Number of activities to retrieve per API request (default is 200).

        Returns:
            list: A complete list of all activity records retrieved from the API.
        """
        if access_token is None:
            access_token = self.access_token
        page = 1
        data = []
        page_data = ['']
        while len(page_data) > 0:
            self.logger.info(f'Collecting data from page: {page}')

            # Fetch data for specific page
            page_data = self.get_activity_data(
                access_token=access_token,
                per_page=per_page,
                page=page)

            # Append page data to previous data already collected
            data.extend(page_data)

            # Increment page number
            page = page + 1

        return data

    def filter_out_coastal_path_data(
            self,
            activity_data: pd.DataFrame) -> list:
        """
        Filters activity data to extract entries related to the coastal path.

        This method scans the input DataFrame and returns a list of records where
        the activity name contains the 'WCP' tag, indicating it is part of the Wales
        Coast Path.

        Parameters:
        ----------
        activity_data : pd.DataFrame
            A DataFrame containing Strava activity data. Each row should have a 'name' field.

        Returns:
        -------
        list
            A list of activity records (as dictionaries) related to the coastal path.
        """
        # Filter out coastal path data based on WCP tag in activity name
        coastal_path_data = [data for data in activity_data if 'WCP' in data['name']]

        return coastal_path_data

    def collect_pb_effort_activities(self, activity_data: list, access_token: Optional[str] = None) -> pd.DataFrame:
        """
        Extract personal-best effort activities from Strava activity data and return them as a DataFrame.

        Filters activities matching target distances (5km, 10km, HM), fetches full
        activity details from the Strava API, extracts key fields, and compiles the
        results into a pandas DataFrame.

        Parameters
        ----------
        activity_data : list
            List of activity metadata dictionaries.
        access_token : str, optional
            Strava API access token; defaults to the instance token.

        Returns
        -------
        pd.DataFrame
            DataFrame containing filtered PB effort activity details.
        """
        # Collect pb effort activity ids
        pb_efforts_ids = [k['id'] for k in activity_data
                          if any(dist in k['name'] for dist in ['[5km]', '[10km]', '[HM]'])]

        # Manage access token
        if access_token is None:
            access_token = self.access_token

        # Define request header
        header = {'Authorization': 'Bearer ' + access_token}

        # Iterate through each pb effort activity
        pb_effort_data = []
        for activity_id in pb_efforts_ids:
            # Define activity url
            activities_url = f"https://www.strava.com/api/v3/activities/{activity_id}"

            # Execute request
            data = requests.get(
                url=activities_url,
                headers=header,
            ).json()

            # Fetch official time from data
            data["time"] = data['description'].split("[")[-1].split("]")[0].split(" - ")[-1]

            # Filter down data to keys of interest
            keys_to_keep = {"id", "name", "start_date", "time"}
            filtered_data = {k: data[k] for k in keys_to_keep if k in data}

            # Append activity data to list
            pb_effort_data.append(filtered_data)

        return pd.DataFrame(pb_effort_data)

    def collect_activity_stream_data(self, activity_data: list, vars: Variables, access_token: Optional[str] = None) -> pd.DataFrame:
        """
        """
        # Collect pb effort activity ids
        pb_efforts_ids = [k['id'] for k in activity_data
                          if any(dist in k['name'] for dist in ['[5km]', '[10km]', '[HM]'])]

        # Manage access token
        if access_token is None:
            access_token = self.access_token

        # Define request header
        header = {'Authorization': 'Bearer ' + access_token}

        # Iterate through each pb effort activity
        for activity_id in pb_efforts_ids:
            # Define activity url
            activities_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams"

            params = {
                "keys": "distance,heartrate,time",
                "key_by_type": "true"
            }

            # Execute request
            data = requests.get(
                url=activities_url,
                headers=header,
                params=params
            ).json()

            distance = data.get("distance", {}).get("data", [])
            heartrate = data.get("heartrate", {}).get("data", [])
            time = data.get("time", {}).get("data", [])

            splits = []
            current_split_start_idx = 0
            split_distance = 1000  # meters

            for i in range(1, len(distance)):
                if distance[i] - distance[current_split_start_idx] >= split_distance:
                    split = {
                        "split_number": len(splits) + 1,
                        "start_time": time[current_split_start_idx],
                        "end_time": time[i],
                        "split_time": time[i] - time[current_split_start_idx],
                        "avg_hr": (
                            sum(heartrate[current_split_start_idx:i]) /
                            len(heartrate[current_split_start_idx:i])
                            if heartrate else None
                        )
                    }
                    splits.append(split)
                    current_split_start_idx = i

            self.export_data_as_json(data=splits, vars=vars, container="strava", output_filename=f"stream/{activity_id}.json")

    def export_data_as_json(self, data: list, vars: Variables, container: str, output_filename: str) -> None:
        """
        """
        # Serialize to JSON
        json_data = json.dumps(data)

        # Connect to blob storage account
        blob_service_client = BlobServiceClient.from_connection_string(
            vars.storage_account_conneciton_string
        )

        # Connect to container within the storage account
        blob_client = blob_service_client.get_blob_client(
            container=container,
            blob=output_filename  # e.g. "activity_12345_streams.json"
        )

        # Upload JSON to Azure Blob Storage
        blob_client.upload_blob(
            json_data,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/json")
        )

    def export_data_as_csv(self, df: pd.DataFrame, vars: Variables, container: str, output_filename: str) -> None:
        """
        Export a pandas DataFrame as a CSV file to an Azure Blob Storage container.

        This method converts the provided DataFrame into an in-memory CSV string,
        connects to the Azure Blob Storage account specified in `vars`, and uploads
        the CSV content to the designated container and blob path.

        Parameters:
            df : pd.DataFrame
                The DataFrame to be exported as a CSV file.
            vars : Variables
                An object containing configuration values, including the Azure Storage
                account connection string.
            container : str
                The name of the Azure Blob Storage container where the file will be uploaded.
            output_filename : str
                The name (including path, if applicable) of the CSV file to create in the blob container.

        Returns: None (This method performs an upload and does not return a value.)
        """
        # Convert DataFrame to CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Connect to blob storage account
        blob_service_client = BlobServiceClient.from_connection_string(
            vars.storage_account_conneciton_string)

        # Connect to container within the storage account
        blob_client = blob_service_client.get_blob_client(
            container=container,
            blob=output_filename)

        # Upload CSV to Azure Blob Storage
        blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)

    def export_activity_data(self, data: list, vars: Variables, container: str, output_filename: str) -> None:
        """
        Exports activity data to a CSV file and uploads it to Azure Blob Storage.

        Processes the list of activity dictionaries into a pandas DataFrame, selects
        relevant columns, cleans up the map polyline data, converts the DataFrame
        to CSV format, and uploads the CSV to the specified Azure Blob Storage container.

        Args:
            data (list): A list of activity data dictionaries to export.
            vars (Variables): An instance of the Variables class containing storage account credentials.
            container (str): The name of the Azure Blob Storage container where the file will be uploaded.
            output_filename (str): The name of the output CSV file in the blob storage.
        """
        # Generate pandas dataframe from data collected
        df = pd.DataFrame(data)

        # Remove unwanted columns
        df = df[['id',
                 'name',
                 'distance',
                 'moving_time',
                 'total_elevation_gain',
                 'type',
                 'start_date',
                 'kudos_count',
                 'comment_count',
                 'athlete_count',
                 'map']]

        # Clean up polyline data from map column in dataframe
        df['map'] = df['map'].apply(lambda x: x['summary_polyline'])

        self.export_data_as_csv(df=df, vars=vars, container=container, output_filename=output_filename)
