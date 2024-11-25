# Import python dependencies
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from io import StringIO
import pandas as pd
import json
import os

# Import project dependencies
from functions.variables import Variables

# Collect codebase variables
vars = Variables()

# Create BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

# Get a BlobClient for the specific blob
blob_client = blob_service_client.get_blob_client(container=vars.storage_account_container_name,
                                                  blob='activity_data.csv')

# Download blob content as a stream
blob_data = blob_client.download_blob().readall()

# Convert blob data to a pandas DataFrame
csv_data = StringIO(blob_data.decode('utf-8'))
df = pd.read_csv(csv_data)

# Create data the directory
if not os.path.exists('data'):
    os.makedirs('data')

# Update local activity data
df.to_csv('data/activity_data.csv', index=False)

# Construct json payload
data = {
    'last_updated': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
}

# Write the JSON object to a file
with open('data/last_updated.json', "w") as file:
    json.dump(data, file, indent=4)
