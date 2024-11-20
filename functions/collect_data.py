from functions.variables import Variables

from azure.storage.blob import BlobServiceClient
from io import StringIO
import pandas as pd
import requests
import json

def get_activity_data(access_token: str,
                      per_page: int = 200,
                      page: int = 1) -> list:
    '''
    Input: Access token, per_page and page number
    Output: Activity Data for given page
    Function to collect strava activity data for a given page number
    '''
    # Define activity url
    activities_url = "https://www.strava.com/api/v3/athlete/activities"

    # Define request header and paramaters
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': page}

    # Execute request
    data = requests.get(
        url=activities_url,
        headers=header,
        params=param
    ).json()

    return data

def collect_all_activity_data(access_token: str,
                              per_page: int) -> list:
    '''
    Input: Access token and number of activities per page
    Output: Activity Data
    Function to iterate through all pages and return all activity data
    '''
    page = 1
    data = []
    page_data = ['']
    while len(page_data) > 0:

        # Fetch data for specific page
        page_data = get_activity_data(access_token, per_page, page)

        # Append page data to previous data already collected
        data.extend(page_data)

        # Increment page number
        page = page + 1

    return data


def export_activity_data(data: list,
                         vars: Variables,
                         container: str,
                         output_filename: str) -> None:
    '''
    Input: Activity data, project variables, blob container name and filename
    Output: None
    Function to export data as csv to local file store
    '''
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
    blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

    # Connect to container within the storage account
    blob_client = blob_service_client.get_blob_client(container=container, blob=output_filename)

    # Upload CSV to Azure Blob Storage
    blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)


def read_activity_data(vars: Variables) -> pd.DataFrame:
    '''
    Input: Project variables object
    Output: Activity Data Dataframe
    Function to read activity data dataframe from local file store
    '''
    if vars.use_local_storage:

        # Read activity data from local file store
        with open('data/activity_data.csv', 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)

    else:

        # Create BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

        # Get a BlobClient for the specific blob
        blob_client = blob_service_client.get_blob_client(container=vars.storage_account_container_name,
                                                          blob='activity_data.csv')

        # Download blob content as a stream
        blob_data = blob_client.download_blob().readall()

        # Convert blob data to a pandas DataFrame
        csv_data = StringIO(blob_data.decode('utf-8'))
        df = pd.read_csv(csv_data)

    # Cast date as pandas datatime object
    df['start_date'] = pd.to_datetime(df['start_date'])

    return df


def read_data_metadata(vars: Variables) -> dict:
    '''
    Input: Project Variables Object
    Output: Json payload of project metadata
    Function to read project metadata
    '''
    if vars.use_local_storage:
        with open('data/last_updated.json') as f:
            data = json.load(f)

        return data

    else:

        # Create BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

        # Get a BlobClient for the specific blob
        blob_client = blob_service_client.get_blob_client(container=vars.storage_account_container_name,
                                                          blob='last_updated.json')

        # Download blob content as a stream
        blob_data = blob_client.download_blob().readall()

        # Parse JSON content
        data = json.loads(blob_data.decode('utf-8'))

        return data
