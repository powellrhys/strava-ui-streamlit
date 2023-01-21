import requests

def get_data(access_token, per_page=200, page=1):

    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': page}
   
    data = requests.get(
        activites_url, 
        headers=header, 
        params=param
    ).json()

    return data