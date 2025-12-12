# Import dependencies
from frontend.functions.navigation import get_navigation
from unittest.mock import patch, MagicMock
import unittest

class TestGetNavigation(unittest.TestCase):

    @patch('frontend.functions.navigation.st')
    def test_get_navigation(self, mock_st):
        """
        Test behaviour of the updated frontend navigation
        """

        # Prepare mock return for st.navigation
        mock_nav = MagicMock(name="navigation")
        mock_st.navigation.return_value = mock_nav

        # Mock st.Page to return predictable values
        mock_st.Page.side_effect = lambda *args, **kwargs: {"args": args, "kwargs": kwargs}

        # Call function
        result = get_navigation()

        # --- Validate st.Page calls ---
        expected_page_calls = [
            # Overview
            ((), {"page": "pages/home.py", "title": "Home"}),
            (("pages/activities.py",), {"title": "Activity Overview"}),
            (("pages/progress.py",), {"title": "Progress Overview"}),

            # HeatMap
            (("pages/heatmap.py",), {"title": "Strava Heatmap"}),
            (("pages/coastal_path.py",), {"title": "Coastal Path"}),

            # Running
            (("pages/pb_efforts.py",), {"title": "PB Efforts Overview"}),
        ]

        actual_calls = mock_st.Page.call_args_list
        self.assertEqual(len(actual_calls), len(expected_page_calls))

        for actual_call, expected_call in zip(actual_calls, expected_page_calls):
            self.assertEqual(actual_call[0], expected_call[0])
            self.assertEqual(actual_call[1], expected_call[1])

        # --- Validate st.navigation call ---
        # Recreate expected pages dict using the mocked return values
        expected_pages = {
            "Overview": [
                {"args": (), "kwargs": {"page": "pages/home.py", "title": "Home"}},
                {"args": ("pages/activities.py",), "kwargs": {"title": "Activity Overview"}},
                {"args": ("pages/progress.py",), "kwargs": {"title": "Progress Overview"}},
            ],
            "HeatMap": [
                {"args": ("pages/heatmap.py",), "kwargs": {"title": "Strava Heatmap"}},
                {"args": ("pages/coastal_path.py",), "kwargs": {"title": "Coastal Path"}},
            ],
            "Running": [
                {"args": ("pages/pb_efforts.py",), "kwargs": {"title": "PB Efforts Overview"}},
            ],
        }

        mock_st.navigation.assert_called_once_with(expected_pages)

        # --- Verify return value ---
        self.assertEqual(result, mock_nav)
