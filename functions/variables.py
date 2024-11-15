from dotenv import load_dotenv
import datetime as dt
import os

load_dotenv()

class Variables:
    '''
    Input: None
    Output: None
    Class to hold all codebase constants
    '''
    def __init__(self):

        # Date related variables
        self.current_year = dt.date.today().year
        self.previous_year = dt.date.today().year - 1
        self.first_activity_date = dt.datetime(2016, 1, 1)
        self.current_date = dt.datetime(dt.datetime.now().year, 12, 31)

        # API related variables
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.redirect_url = os.getenv('REDIRECT_URI')
