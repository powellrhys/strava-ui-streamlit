# Import Selenium dependencies
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import warnings
import logging

from functions.authentication import \
    get_authorization_url

from functions.variables import \
    Variables

from functions.server import \
    configure_driver

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

# Configure Selenium Driver
driver = configure_driver(driver_path=vars.driver_path,
                          headless=True)
logger.info('Selenium Driver Configured')

# Generate auth url and redirect to authentication page
auth_url = get_authorization_url(CLIENT_ID=vars.client_id,
                                 REDIRECT_URI=vars.redirect_url)
logger.info('Authentication URL generated')

# Navigate to auth url
driver.get(auth_url)
logger.info('Navigate to auth url completed')

# Enter email into login form
WebDriverWait(driver, 10) \
    .until(EC.presence_of_element_located((By.ID, 'email')))
driver.find_element(By.ID, 'email').send_keys(vars.strava_username)
logger.info('Strava username entered')

# Enter Password into login form
WebDriverWait(driver, 10) \
    .until(EC.presence_of_element_located((By.ID, 'password')))
driver.find_element(By.ID, 'password').send_keys(vars.strava_password)
logger.info('Strava password entered')

# Click Submit on login form
WebDriverWait(driver, 10) \
    .until(EC.presence_of_element_located((By.ID, "login-button")))
driver.find_element(By.ID, "login-button").click()
logger.info('Login button clicked')

# Click Submit on login form
WebDriverWait(driver, 10) \
    .until(EC.presence_of_element_located((By.ID, "authorize")))
driver.find_element(By.ID, "authorize").click()
logger.info('Strava api authorization completed')

# Wait until the target text appears in the <body> tag
logger.info('Collecting strava activity data...')
target_text = 'All Activity Data Collected'
WebDriverWait(driver, 30).until(
    lambda d: target_text in d.find_element(By.TAG_NAME, "body").text
)
logger.info('Strava activity data collected')

driver.quit()
