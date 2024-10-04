import datetime as dt

class Variables:
    '''
    Input: None
    Output: None
    Class to hold all codebase constants
    '''
    def __init__(self):

        self.current_year = dt.date.today().year
        self.previous_year = dt.date.today().year - 1
