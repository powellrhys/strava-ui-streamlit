# Import dependencies
from backend.functions.clients.strava_client import StravaClient

class ActivitiesService(StravaClient):
    """
    """
    def collect_all_activity_data(self, access_token: str, per_page: int = 200) -> list:
        """
        Retrieves all athlete activity data from the Strava API by paginating through results.

        This method continuously fetches activity data page by page until no more activities
        are returned, aggregating all results into a single list.

        Args:
            access_token (Optional[str]): The access token for API authorization. If None,
                                        the instance's stored access token will be used.
            per_page (int): Number of activities to retrieve per API request (default is 200).

        Returns:
            list: A complete list of all activity records retrieved from the API.
        """
        if access_token is None:
            access_token = self.access_token
        page = 1
        data = []
        page_data = ['']
        while len(page_data) > 0:
            self.logger.info(f'Collecting data from page: {page}')

            # Fetch data for specific page
            page_data = self.get_activity_data(access_token=access_token, per_page=per_page, page=page)

            # Append page data to previous data already collected
            data.extend(page_data)

            # Increment page number
            page = page + 1

        return data
