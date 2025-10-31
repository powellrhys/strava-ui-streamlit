# Import dependencies
from backend.functions.authentication import exchange_code_for_token
from backend.functions.data_functions import Variables
import urllib.parse
import webbrowser

# Import project variables
vars = Variables()

# Define access token scope
scopes = [
    "read",
    "profile:read_all",
    "activity:read_all",
    "activity:write"
]

# Define auth url
auth_url = (
    f"https://www.strava.com/oauth/authorize"
    f"?client_id={vars.client_id}"
    f"&redirect_uri={urllib.parse.quote('http://localhost/')}"
    f"&response_type=code"
    f"&scope={','.join(scopes)}"
    f"&approval_prompt=force"
)

# Open manual authentication url
webbrowser.open(auth_url)

# Prompt user to input authorization code
code = input('Please enter returned authorization code: ')

# Exchange code for access token
access_token = exchange_code_for_token(
    client_id=vars.client_id,
    client_secret=vars.client_secret,
    code=code
)

# Print refresh token
print(access_token['refresh_token'])
