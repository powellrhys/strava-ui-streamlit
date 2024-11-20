from fastapi.middleware.cors import CORSMiddleware
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from azure.storage.blob import BlobServiceClient
from selenium import webdriver
from datetime import datetime
from fastapi import FastAPI
import json

from functions.variables import \
    Variables


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


def export_data_metadata(vars: Variables,
                         container: str,
                         output_filename: str) -> None:
    '''
    Input: None
    Output: None
    Function to update the data metadata file
    '''
    # Construct json payload
    data = {
        'last_updated': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }

    json_object = json.dumps(data)

    blob_service_client = BlobServiceClient.from_connection_string(vars.storage_account_conneciton_string)

    # Upload CSV to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=container, blob=output_filename)

    blob_client.upload_blob(json_object, overwrite=True)


def configure_driver(driver_path: str = 'chromedriver.exe',
                     headless: bool = False) -> WebDriver:

    # Configure logging to suppress unwanted messages
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                                "AppleWebKit/537.36 (KHTML, like Gecko)",
                                "Chrome/114.0.5735.199 Safari/537.36")

    if headless:
        chrome_options.add_argument("--headless")

    # Configure Driver with options
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    return driver
