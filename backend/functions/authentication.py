from typing import Optional
import requests

def exchange_code_for_token(client_id: str,
                            client_secret: str,
                            code: str) -> Optional[str]:
    """
    Exchanges an authorization code for an access token using Strava's OAuth API.

    Parameters:
        client_id (str): The application's client ID provided by Strava.
        client_secret (str): The application's client secret provided by Strava.
        code (str): The authorization code received from the Strava authorization redirect.

    Returns:
        Optional[str]: The access token as a JSON string if the exchange is successful,
                       otherwise None.
    """
    # Define token url
    token_url = "https://www.strava.com/api/v3/oauth/token"

    # Define request payload
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }

    # Execute request
    response = requests.post(token_url, data=payload)

    # Decode and return response
    if response.status_code == 200:
        return response.json()
    else:
        return None
