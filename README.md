# strava-ui-streamlit

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![PowerShell](https://img.shields.io/badge/powershell-239120?style=for-the-badge&logo=powershell&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)


The strava-ui-streamlit repository is a python project created to illustrate personal athlete data from [Strava](https://www.strava.com/). Visuals are generated using a combination of [folium](https://python-visualization.github.io/folium/) and [plotly](https://plotly.com/python/) and are rendered using [streamlit](https://streamlit.io/). Data is collected using the [Strava Developers APIs](https://developers.strava.com/docs/reference/).

## Backend

The backend uses the [Strava Developers APIs](https://developers.strava.com/docs/reference/) to fetch personal athlete data from strava. Data scrapping occurs weekly, orchestrated by the `collect_data.yml` github action. 

## Frontend

The frontend is written in python and uses the streamlit library. The frontend consists 4 pages (illustrated below) and uses data from an azure blob storage account to render various tables and plots.

Given the private nature of the data, access to the application is limited and is handled by oauth0.

The application has been deployed twice:

- [Azure](https://strava-streamlit-frontend.azurewebsites.net/)
- [Streamlit Cloud](https://strava-frontend.streamlit.app/)


### Home Page

![Screenshot of Home Page](docs/assets/home_page.png?raw=true "Home Page")

### Activities Page

![Screenshot of Activity Page](docs/assets/activities_page.png?raw=true "Activity Page")

### Heatmap Page

![Screenshot of Heatmap Page](docs/assets/heatmap_page.png?raw=true "Heatmap Page")

### Progress Page

![Screenshot of Progress Page](docs/assets/progress_page.png?raw=true "Progress Page")

### Coastal Path Page

![Screenshot of Coastal Path Page](docs/assets/coastal_path_page.png?raw=true "Coastal Path Page")
