import pandas as pd
import requests

def get_activity_data(access_token: str,
                      per_page: int = 200,
                      page: int = 1) -> list:

    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': page}

    data = requests.get(
        url=activities_url,
        headers=header,
        params=param
    ).json()

    return data

def collect_all_activity_data(access_token: str,
                              per_page: int) -> list:

    page = 1
    data = []
    page_data = ['']
    while len(page_data) > 0:

        page_data = get_activity_data(access_token, per_page, page)

        data.extend(page_data)

        page = page + 1

    return data

def export_activity_data(data: list,
                         output_directory: str,
                         output_filename: str):

    df = pd.DataFrame(data)
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

    df['map'] = df['map'].apply(lambda x: x['summary_polyline'])
    df.to_csv(f'{output_directory}/{output_filename}')
