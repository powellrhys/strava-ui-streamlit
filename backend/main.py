from fastapi import Request
import uvicorn

from functions.authentication import \
    exchange_code_for_token

from functions.collect_data import \
    collect_all_activity_data, \
    export_activity_data

from functions.server import \
    export_data_metadata, \
    configure_server

from functions.variables import \
    Variables

# Load environmental variables
vars = Variables()
# Configure backend API
app = configure_server()

# Define Root Endpoint
@app.get('/')
def home():
    return {'Server Running': True}

# Define callback endpoint
@app.get('/callback')
def callback(req: Request):

    # Fetch code from callback url
    code = req.query_params['code']
    if code:

        # Fetch token from code
        token_data = exchange_code_for_token(vars.client_id,
                                             vars.client_secret,
                                             code)

        if token_data:

            # Collect activity data
            data = collect_all_activity_data(access_token=token_data['access_token'],
                                             per_page=200)

            # Export data as csv to local file store
            export_activity_data(data=data,
                                 output_directory='data',
                                 output_filename='temp_activity_data.csv')

            # Update last updated metadata
            export_data_metadata()

            return 'All Activity Data Collected'

        else:
            return "Failed to retrieve access token."
    else:
        return "Authorization code not found."


if __name__ == '__main__':

    # Run Backend Server
    uvicorn.run(app, host="0.0.0.0", port=5000)
