# Import dependencies
from backend.functions.data_functions import ApiService, Variables
import warnings
import logging

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
activity_data = app.collect_all_activity_data()
logger.info("Activity Data collected \n")

app.collect_activity_stream_data(activity_data=activity_data, vars=vars)

# # Collect and export pb effort data
# logger.info("Collecting and exporting pb effort data...")
# pb_effort_data = app.collect_pb_effort_activities(activity_data=activity_data)
# app.export_data_as_csv(df=pb_effort_data,
#                        vars=vars,
#                        container='strava',
#                        output_filename='pb_effort_data.csv')
# logger.info("PB effort data exported \n")

# # Filter out activity data
# logger.info("Filter out coastal path activities...")
# costal_path_data = app.filter_out_coastal_path_data(activity_data=activity_data)
# logger.info("Coastal path data filtered out \n")

# # Export activity data to blob storage
# logger.info("Exporting activity data...")
# app.export_activity_data(data=activity_data,
#                          vars=vars,
#                          container='strava',
#                          output_filename='activity_data.csv')
# logger.info("Data exported to blob storage \n")

# # Export coastal path data to blob storage
# logger.info("Exporting coastal path data...")
# app.export_activity_data(data=costal_path_data,
#                          vars=vars,
#                          container='strava',
#                          output_filename='coastal_path_data.csv')
# logger.info("Data exported to blob storage \n")
