# Import dependencies
import pandas as pd
import requests

class WelshCoastalPathService:
    """
    """
    def collect_wcp_segments(self, access_token: str, per_page: int = 200, page: int = 1) -> pd.DataFrame:
        """
        """
        # Define activity url
        activities_url = "https://www.strava.com/api/v3/segments/starred"

        # Define request header and parameters
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': per_page, 'page': page}

        # Execute request
        data = requests.get(url=activities_url, headers=header, params=param).json()

        # Filter out not wcp segments
        wcp_segments = [segment for segment in data if "WCP" in segment["name"]]

        # Create list of wcp segments
        wcp_data = []
        for wcp_segment in wcp_segments:
            wcp_data.append(
                {
                    "id": wcp_segment["id"],
                    "name": wcp_segment["name"],
                    "polyline": self.collect_wcp_polyline(id=wcp_segment["id"], access_token=access_token)
                }
            )

        return pd.DataFrame(wcp_data)

    def collect_wcp_polyline(self, id: int, access_token: str) -> str:
        """
        """
        # Define activity url
        activities_url = f"https://www.strava.com/api/v3/segments/{id}"

        # Define request header and parameters
        header = {'Authorization': 'Bearer ' + access_token}

        # Execute request
        data = requests.get(url=activities_url, headers=header).json()

        return data["map"]["polyline"]

    def filter_out_coastal_path_data(self, activity_data: pd.DataFrame) -> list:
        """
        Filters activity data to extract entries related to the coastal path.

        This method scans the input DataFrame and returns a list of records where
        the activity name contains the 'WCP' tag, indicating it is part of the Wales
        Coast Path.

        Parameters:
        ----------
        activity_data : pd.DataFrame
            A DataFrame containing Strava activity data. Each row should have a 'name' field.

        Returns:
        -------
        list
            A list of activity records (as dictionaries) related to the coastal path.
        """
        # Filter out coastal path data based on WCP tag in activity name
        coastal_path_data = [data for data in activity_data if 'WCP' in data['name']]

        return coastal_path_data
