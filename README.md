# strava-ui-streamlit

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

The strava-ui-streamlit repository is a python project created to illustrate personal athlete data from [Strava](https://www.strava.com/). Visuals are generated using a combination of [folium](https://python-visualization.github.io/folium/) and [plotly](https://plotly.com/python/) and are rendered using [streamlit](https://streamlit.io/). Data is collected using the [Strava Developers APIs](https://developers.strava.com/docs/reference/) and is returned to the user using a FastAPI web server. 

In its current state, the project is only able to run locally with data being stored in a localy csv file. 

### Prerequisites

To successfully run this project locally the following conditions must be met:

- Ensure all python requirements are installed. This can be done by running `pip install -r requirements.txt`
- Make sure your Strava account supports an API application. More information on how to configure this can be found [here](https://developers.strava.com/).
- Once your Strava account has an API application, make sure you have a local environmental variables (.env) file. In it should be the following variables:
    - `CLIENT_ID` - available from your API application dashboard page
    - `CLIENT_SECRET` - available from your API application dashboard page
    - `REDIRECT_URI` - should be `'http://localhost:5000/callback'` when running the project locally
    - `APP_USERNAME` - can be anything, used when first loading up the page
    - `APP_PASSWORD` - can be anything, used when first loading up the page
    - `STORAGE_ACCOUNT_CONNECTION_STRING` - The connection string for your azure blob storage account (only applicable if not using local storage)
    - `STORAGE_ACCOUNT_CONTAINER_NAME` - The container name where the data is stored (only applicable if not using local storage)
    - `USE_LOCAL_STORAGE` - Flag to indicate whether data is being collected from your local file store or from an azure blob storage container. This value will default to `False`, forcing the application to pull data from the connected storage account.
    - `LOGIN_REQUIRED` - Flag to determine whether the user needs to login to see the page content. The value will default to `True` if not specified. For development purposes, it's useful to override this value with `False`.
    - `GITHUB_ACCESS_TOKEN` - PAT token taken from github to trigger the data collection github action.  

### Running the Project

Data is collected via an input button on the landing page. Therefore, to first collect data, the frontend must be launched. This can be done by running the following command from the root directory of the project.

`streamlit run Home.py`

Data is collected via a github action. To trigger this action from the frontend, a github PAT token is required and should be stored under the `GITHUB_ACCESS_TOKEN` environmental variable. This pipeline stores all necessary data in an azure blob storage account for which an `STORAGE_ACCOUNT_CONNECTION_STRING` and `STORAGE_ACCOUNT_CONTAINER_NAME` are required. To collect data from your own account, a similar setup is required. 

### Project Overview

In its current state the project has 4 pages:

- Home - An overview of yearly stats. The activity types illustrated can be edited to meet your requirements
- Activities - The data collected displayed in tabular format
- Heatmap - A control panel enabling the user to customize their activity heatmap
- Progress - Visualisations of activity progress over the years

The application has been deployed [here](strava-streamlit-frontend.azurewebsites.net), however is protected behind a login page. An overview of the pages can be seen below:

#### Home Page

![Screenshot of Home Page](assets/home_page.png?raw=true "Home Page")

#### Activities Page

![Screenshot of Activity Page](assets/activities_page.png?raw=true "Activity Page")

#### Heatmap Page

![Screenshot of Heatmap Page](assets/heatmap_page.png?raw=true "Heatmap Page")

#### Progress Page

![Screenshot of Progress Page](assets/progress_page.png?raw=true "Progress Page")
