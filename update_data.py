from dotenv import load_dotenv
from fastapi import Request
import webbrowser
import uvicorn
import os

from functions.authentication import \
    exchange_code_for_token, \
    get_authorization_url


from functions.collect_data import \
    collect_all_activity_data, \
    export_activity_data

from functions.server import \
    configure_server

# Load environmental variables
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Configure backend API
app = configure_server()

# Define callback endpoint
@app.get('/callback')
def callback(req: Request):

    # Fetch code from callback url
    code = req.query_params['code']
    if code:

        # Fetch token from code
        token_data = exchange_code_for_token(CLIENT_ID, CLIENT_SECRET, code)

        if token_data:

            # Collect activity data
            data = collect_all_activity_data(access_token=token_data['access_token'],
                                             per_page=200)

            # Export data as csv to local file store
            export_activity_data(data=data,
                                 output_directory='data',
                                 output_filename='activity_data.csv')

            return 'All Activity Data Collected'

        else:
            return "Failed to retrieve access token."
    else:
        return "Authorization code not found."


if __name__ == '__main__':

    # Open the authorization URL in the default browser
    auth_url = get_authorization_url(CLIENT_ID, REDIRECT_URI)
    webbrowser.open(auth_url)

    # Run Backend Server
    uvicorn.run(app, host="0.0.0.0", port=5000)
