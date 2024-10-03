from typing import Optional
import requests

def get_authorization_url(CLIENT_ID: str,
                          REDIRECT_URI: str) -> str:

    authorization_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=profile:read_all,activity:read_all"
    )
    return authorization_url

def exchange_code_for_token(CLIENT_ID: str,
                            CLIENT_SECRET: str,
                            code: str) -> Optional[str]:

    token_url = "https://www.strava.com/api/v3/oauth/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None
