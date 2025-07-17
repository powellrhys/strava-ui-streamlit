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
    refresh_token=vars.refresh_token,
    logger=logger
)
logger.info("Api service configured \n")

# Collect access token to hit api
logger.info("Collecting access token...")
app.collect_access_token()
logger.info("Access token collected \n")

# Collect activity data
logger.info("Collecting activity data...")
data = app.collect_all_activity_data()
logger.info("Activity Data collected \n")

# Export data to blob storage
logger.info("Exporting data...")
app.export_activity_data(data=data,
                         vars=vars,
                         container='strava',
                         output_filename='activity_data.csv')
logger.info("Data exported to blob storage \n")
