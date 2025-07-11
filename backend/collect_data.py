# Import python dependencies
import warnings
import logging

# Import project dependencies
from functions.data_functions import (
    ApiService,
    Variables
)

# Ignore warnings
warnings.filterwarnings("ignore")

# Configure Logger
logger = logging.getLogger('BASIC')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# Collect codebase variables
vars = Variables()

# Configure API service class
logger.info("Configuring API service application...")
app = ApiService(
    client_id=vars.client_id,
    client_secret=vars.client_secret,
    refresh_token=vars.refresh_token
)
logger.info("Api service configured \n")

logger.info("Collecting access token...")
app.collect_access_token()
logger.info("Access token collected \n")

# logger.info("Collecting activity data...")
# app.collect_all_activity_data()
# logger.info("Activity Data collected \n")

# logger.info("Exporting data...")
# app.collect_access_token()
# logger.info("Data exported to blob storage \n")
