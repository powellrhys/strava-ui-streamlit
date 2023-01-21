import requests

def authorization(client_id, redirect_uri):

    request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                    f'&response_type=code&redirect_uri={redirect_uri}' \
                    f'&approval_prompt=force' \
                    f'&scope=profile:read_all,activity:read_all'
    return request_url

def get_access_token(client_id, client_secret, code):

    token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                        data={'client_id': client_id,
                                'client_secret': client_secret,
                                'code': code,
                                'grant_type': 'authorization_code'})

    access_token = token.json()['access_token']

    return access_token