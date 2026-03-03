# Import dependencies and modules
from azure.storage.blob import BlobServiceClient
from .variables import Variables
from io import StringIO
import pandas as pd
import requests
import logging
import zipfile
import io

class MountainService:
    """
    A service class responsible for managing mountain-related data and operations.
    """
    def __init__(self, logger: logging.Logger) -> None:
        """
        Initializes the MountainService with a logger.
        """
        self.logger = logger

    def _collect_mountain_data(self) -> bytes:
        """
        Downloads the ZIP file containing mountain data and returns its content as bytes.
        """
        # Declare the URL for the ZIP file download
        url = "https://www.hill-bagging.co.uk/dobih-downloads/hillcsv.zip"

        # Download the zip file stream from the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content

    def _extract_csv_from_zip(self, zip_bytes: bytes) -> bytes:
        """
        Extracts the first CSV file found in the ZIP archive and returns its content as bytes.
        """
        # Use zipfile to read the ZIP content from bytes and extract the CSV file
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            csv_files = [f for f in z.namelist() if f.lower().endswith(".csv")]
            if not csv_files:
                raise ValueError("No CSV file found inside ZIP archive")

            # Collect the first CSV file found and return its content as bytes
            csv_filename = csv_files[0]
            self.logger.info(f"Extracting {csv_filename} from ZIP")
            return z.read(csv_filename)

    def _load_dataframe(self, csv_bytes: bytes) -> pd.DataFrame:
        """
        Loads CSV bytes into a pandas DataFrame.
        """
        return pd.read_csv(io.BytesIO(csv_bytes))

    def _transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the DataFrame by filtering and selecting relevant columns.
        """
        # Filter out unwanted columns and rows based on criteria
        columns_to_keep = ["Name", "Metres", "Feet", "Country", "County", "Latitude", "Longitude"]
        df = df[columns_to_keep]

        # Apply filters: Only include mountains over 100 meters
        if "Metres" in df.columns:
            df = df[df["Metres"] > 100]

        # Apply filters: Only include mountains located in Wales (Country code "W")
        if "Country" in df.columns:
            df = df[df["Country"] == "W"]

        return df.sort_values(by="Metres", ascending=False)

    def export_data_as_csv(self, df: pd.DataFrame, vars: Variables, container: str, output_filename: str) -> None:
        """
        Exports the transformed DataFrame as a CSV file to Azure Blob Storage.
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

    def run(self):
        """
        Main method to execute the data collection, transformation, and export process.
        """
        try:
            # Download and process mountain data
            zip_content = self._collect_mountain_data()

            # Extract CSV from ZIP content
            csv_content = self._extract_csv_from_zip(zip_content)

            # Convert CSV bytes to DataFrame
            df = self._load_dataframe(csv_content)
            self.logger.info(f"Loaded dataframe with {len(df)} rows")

            # Transform the DataFrame by filtering and selecting relevant columns
            df = self._transform_dataframe(df)
            self.logger.info(f"After filtering: {len(df)} rows")

            # Export the transformed DataFrame as a CSV file to Azure Blob Storage
            self.export_data_as_csv(df=df, vars=Variables(), container='strava',
                                    output_filename='welsh_mountain_data.csv')

        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise
