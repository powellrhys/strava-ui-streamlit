import requests

def trigger_update_dat_github_action(access_token: str,
                                     ref: str = 'main') -> dict:
    '''
    Input: Access token and branch reference
    Output: Request response
    Function to trigger github action
    '''
    # Define request url
    url = "https://api.github.com/repos/powellrhys/strava-ui-streamlit/actions/workflows/update-data.yml/dispatches"

    # Define request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Define request parameters
    payload = {
        "ref": ref
    }

    # Execute post request
    response = requests.post(url, json=payload, headers=headers)

    # Handle response
    if response.status_code == 204:
        print("Workflow triggered successfully!")
    else:
        print(f"Failed to trigger workflow: {response.status_code} {response.text}")

    return response.json() if response.content else {}


def get_latest_workflow_run_id(access_token: str) -> int:
    '''
    Input: Access token
    Output: Workflow run id
    Function to collect latest workflow run id
    '''
    # Define endpoint url
    url = "https://api.github.com/repos/powellrhys/strava-ui-streamlit/actions/workflows/update-data.yml/runs"

    # Define request header
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Execute request
    response = requests.get(url, headers=headers)

    # Handle failed request
    if response.status_code != 200:
        print(f"Error fetching workflow runs: {response.status_code} {response.text}")
        return None

    # Handle successful request
    runs = response.json().get("workflow_runs", [])
    if not runs:
        print("No workflow runs found.")
        return None

    # Return the ID of the most recent workflow run
    return runs[0].get("id")


def monitor_github_action(access_token: str,
                          workflow_run_id: int) -> requests:
    '''
    Input: Access token, workflow run id and polling frequency
    Output: Request response
    Function to monitor github action status
    '''
    # Define endpoint url
    url = f"https://api.github.com/repos/powellrhys/strava-ui-streamlit/actions/runs/{workflow_run_id}"

    # Define request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Execute request
    response = requests.get(url, headers=headers)

    return response
