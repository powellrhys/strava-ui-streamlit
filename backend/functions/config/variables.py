from dotenv import load_dotenv
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
