from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from typing import Optional
from io import StringIO
import pandas as pd
import requests
import os

load_dotenv()

class Variables:
    '''
    Input: None
    Output: None
    Class to hold all codebase constants
    '''
    def __init__(self):

        # API related variables
        self.client_id = os.getenv('client_id')
        self.client_secret = os.getenv('client_secret')
        self.refresh_token = os.getenv('refresh_token')

        # Storage account variables
        self.storage_account_conneciton_string = os.getenv('blob_connection_string')


class ApiService:
    """
    """
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            refresh_token: str) -> None:
        """
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def collect_access_token(self) -> Optional[str]:
        """
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
        """
        if access_token is None:
            access_token = self.access_token
        page = 1
        data = []
        page_data = ['']
        while len(page_data) > 0:

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

    def export_activity_data(
            self,
            data: list,
            vars: Variables,
            container: str,
            output_filename: str) -> None:
        """
        """
        # Generate pandas dataframe from data collected
        df = pd.DataFrame(data)

        # Remove unwanted columns
        df = df[['name',
                 'distance',
                 'moving_time',
                 'total_elevation_gain',
                 'type',
                 'start_date',
                 'kudos_count',
                 'comment_count',
                 'athlete_count',
                 'map',
                 'average_watts']]

        # Clean up polyline data from map column in dataframe
        df['map'] = df['map'].apply(lambda x: x['summary_polyline'])

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
