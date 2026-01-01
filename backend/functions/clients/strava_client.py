# Import dependencies
from typing import Optional
import requests
import logging

class StravaClient:
    """
    """
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, logger: logging.Logger) -> None:
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
        """
        response = requests.post(
            url='https://www.strava.com/api/v3/oauth/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
        )

        tokens = response.json()
        access_token = tokens['access_token']

        return access_token, tokens

    def get_activity_data(self, access_token: str, per_page: int = 200, page: int = 1) -> list:
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
        # Define activity url
        activities_url = "https://www.strava.com/api/v3/athlete/activities"

        # Define request header and parameters
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': per_page, 'page': page}

        # Execute request
        data = requests.get(url=activities_url, headers=header, params=param).json()

        return data
