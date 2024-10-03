import pandas as pd
import requests

def get_activity_data(access_token: str,
                      per_page: int = 200,
                      page: int = 1) -> list:
    '''
    Input: Access token, per_page and page number
    Output: Activity Data for given page
    Function to collect strava activity data for a given page number
    '''
    # Define activity url
    activities_url = "https://www.strava.com/api/v3/athlete/activities"

    # Define request header and paramaters
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': page}

    # Execute request
    data = requests.get(
        url=activities_url,
        headers=header,
        params=param
    ).json()

    return data

def collect_all_activity_data(access_token: str,
                              per_page: int) -> list:
    '''
    Input: Access token and number of activities per page
    Output: Activity Data
    Function to iterate through all pages and return all activity data
    '''
    page = 1
    data = []
    page_data = ['']
    while len(page_data) > 0:

        # Fetch data for specific page
        page_data = get_activity_data(access_token, per_page, page)

        # Append page data to previous data already collected
        data.extend(page_data)

        # Increment page number
        page = page + 1

    return data

def export_activity_data(data: list,
                         output_directory: str,
                         output_filename: str):
    '''
    Input: Activity data, output directory and filename
    Output: CSV written to local file store
    Function to export data as csv to local file store
    '''
    # Generate pandas dataframe from data collected
    df = pd.DataFrame(data)

    # Remove unwanted columns
    df = df[['name',
             'distance',
             'moving_time',
             'total_elevation_gain',
             'type',
             'start_date',
             'kudos_count',
             'comment_count',
             'athlete_count',
             'map',
             'average_watts']]

    # Clean up polyline data from map column in dataframe
    df['map'] = df['map'].apply(lambda x: x['summary_polyline'])

    # Write dataframe to blob storage
    df.to_csv(f'{output_directory}/{output_filename}')
