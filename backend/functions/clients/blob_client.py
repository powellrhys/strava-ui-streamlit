# Import dependencies
from azure.storage.blob import BlobServiceClient, ContentSettings
from backend.functions.config.variables import Variables
from io import StringIO
import pandas as pd
import json

class BlobClient:
    """
    """
    def export_data_as_json(self, data: list, vars: Variables, container: str, output_filename: str) -> None:
        """
        """
        # Serialize to JSON
        json_data = json.dumps(data)

        # Connect to blob storage account
        blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

        # Connect to container within the storage account
        blob_client = blob_service_client.get_blob_client(container=container, blob=output_filename)

        # Upload JSON to Azure Blob Storage
        blob_client.upload_blob(json_data, overwrite=True,
                                content_settings=ContentSettings(content_type="application/json"))

    def export_data_as_csv(self, df: pd.DataFrame, vars: Variables, container: str, output_filename: str) -> None:
        """
        """
        # Convert DataFrame to CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Connect to blob storage account
        blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

        # Connect to container within the storage account
        blob_client = blob_service_client.get_blob_client(container=container, blob=output_filename)

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
