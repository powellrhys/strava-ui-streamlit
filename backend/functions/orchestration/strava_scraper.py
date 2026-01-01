# Import dependencies
from backend.functions.config.variables import Variables
from backend.functions.clients.strava_client import StravaClient
from backend.functions.services.activities import ActivitiesService
import warnings
import logging

class StravaScraper:
    """
    """
    def __init__(self):
        """
        """
        self.vars = Variables()
        self.logger = self.configure_logger()

    def configure_logger() -> logging.Logger:
        """
        """
        # Ignore warnings
        warnings.filterwarnings("ignore")

        # Configure Logger
        logger = logging.getLogger('BASIC')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

        return logger

    def run(self):
        """
        """
        # Configure Strava Client
        strava_client = StravaClient(client_id=self.vars.client_id, client_secret=self.vars.client_secret,
                                     refresh_token=self.vars.refresh_token, logger=self.logger)

        # Collect access token to hit api
        self.logger.info("Collecting access token...")
        access_token = strava_client.collect_access_token()
        self.logger.info("Access token collected \n")
