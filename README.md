# strava-ui-streamlit

### Project Codebase

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![PowerShell](https://img.shields.io/badge/powershell-239120?style=for-the-badge&logo=powershell&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Project Github Action Pipelines

![Update Data](https://github.com/powellrhys/strava-ui-streamlit/actions/workflows/update-data.yml/badge.svg)
![Build & Deploy Application](https://github.com/powellrhys/strava-ui-streamlit/actions/workflows/build-and-deploy.yml/badge.svg)

### Codebase Coverage

[![codecov](https://codecov.io/gh/powellrhys/strava-ui-streamlit/graph/badge.svg?token=5GHA73NUGU)](https://codecov.io/gh/powellrhys/strava-ui-streamlit)
![GitHub issues](https://img.shields.io/github/issues/powellrhys/strava-ui-streamlit.svg)

### Codebase structure

```
strava-ui-streamlit
├── .github
│   └── workflows
├── backend
│   ├── functions
├── frontend
│   ├── functions
│   └── pages
├── infra
```

**strava-ui-streamlit** is a full-stack application designed to help athletes visualize and analyze their 
Strava activity data. It automatically collects training data from Strava, stores it securely in the cloud,
and provides interactive dashboards to explore your performance over time.

- Collects personal activity data from **Strava** using the official API.  
- Automates data collection through **GitHub Actions** on a weekly schedule.  
- Stores processed data in **Azure Blob Storage** for secure and scalable access.  
- Provides interactive visualizations and maps via a **Streamlit** frontend.  
- Supports secure authentication with **Auth0** to protect private data.  

## Backend
- Python-based backend integrates with the **Strava Developer API** to retrieve athlete activity data.  
- Scheduled jobs, managed via **GitHub Actions**, automate weekly data collection and updates.  
- Data is processed and uploaded to **Azure Blob Storage**, ensuring reliability and accessibility.  

## Frontend
- Built with **Streamlit** for fast, interactive data visualization.  
- Leverages **Plotly** and **Folium** for dynamic charts and geospatial activity maps.  
- Organized into four pages showcasing training summaries, trends, and individual workout details.  
- Implements **Auth0** authentication to ensure only authorized users can access private data.  

## Infrastructure
- Cloud storage and hosting powered by **Azure** for scalability and security.  
- Deployment and automation managed via **GitHub Actions** workflows.  
- Easily reproducible and extensible setup for deployment or migration.  

## Testing
- **Pytest** for unit and integration testing to ensure code reliability. 


## Deployment

The frontend application has been deployed to both streamlit cloud and to an azure app service. Both resources can be navigated to via the following urls:

- [Azure](https://strava-streamlit-frontend.azurewebsites.net/)
- [Streamlit Cloud](https://strava-frontend.streamlit.app/)

Due to the sensitive nature of the data, both applications are secured behind authentication, powered by oauth0. Renders of the application are illustrated below.

## Frontend Application

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

### PB Effort Overview Page

![Screenshot of PB Effort Overview Page](docs/assets/pb_effort_overview_page.png?raw=true "PB Effort Overview Page")
