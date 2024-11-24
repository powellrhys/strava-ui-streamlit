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
    - `USE_LOCAL_STORAGE` - Flag to indicate whether data is being collected from your local file store or from azure blob storage container

### Running the Project

Data is collected via an input button on the landing page. Therefore, to first collect data, the frontend must be launched. This can be done by running the following command from the root directory of the project.

`streamlit run Home.py`

Before data can be collected the backend server must also be in operation. This can be done by utilising uvicorn. For those using vscode as their IDE, this can be done using the debugger. An example launch.json file can be seen below:

```
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Run Uvicorn",
        "type": "python",
        "request": "launch",
        "module": "uvicorn",
        "args": [
          "backend.main:app",
          "--host",
          "0.0.0.0",
          "--port",
          "5000",
          "--reload"
        ],
        "jinja": true
      }
    ]
  }
```

Now all requirements have been met, navigate to port 8501 within your browser : 

`https://http://localhost:8501/`

### Project Overview

In its current state the project has 4 pages:

- Home - An overview of yearly stats. The activity types illustrated can be edited to meet your requirements
- Activities - The data collected displayed in tabular format
- Heatmap - A control panel enabling the user to customize their activity heatmap
- Progress - Visualisations of activity progress over the years

#### Home Page

![Screenshot of Home Page](assets/home_page.png?raw=true "Home Page")
