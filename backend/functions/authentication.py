from typing import Optional
import requests

def exchange_code_for_token(client_id: str,
                            client_secret: str,
                            code: str) -> Optional[str]:
    '''
    Input: Client ID, Client Secret, auth code
    Output: Function to retrieve access token
    Function to fetch access token
    '''
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
