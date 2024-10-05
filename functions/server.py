from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from datetime import datetime
import json


def configure_server():
    '''
    Input: None
    Output: Fast API server
    Function to configure FAST API server
    '''
    # Set up FastApi Object
    app = FastAPI()

    # Apply required middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def export_data_metadata() -> None:
    '''
    Input: None
    Output: None
    Function to update the data metadata file
    '''
    # Construct json payload
    data = {
        'last_updated': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }

    # Write dictionary to file store
    with open('data/last_updated.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
