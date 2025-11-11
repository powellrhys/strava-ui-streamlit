# Import dependencies
from frontend.functions.navigation import get_navigation
from unittest.mock import patch, MagicMock
import unittest

class TestGetNavigation(unittest.TestCase):

    @patch('frontend.functions.navigation.st')
    def test_get_navigation(self, mock_st):
        """
        Test to inspect the behaviour of the frontend navigation
        """
        # Mock st.Page and st.navigation
        mock_nav = MagicMock(name='navigation')

        # Mock effects
        mock_st.Page.side_effect = lambda path, title: {'path': path, 'title': title}
        mock_st.navigation.return_value = mock_nav

        # Call function
        result = get_navigation()

        # Verify st.Page was called with expected arguments
        expected_calls = [
            (("pages/home.py",), {'title': "Home"}),
            (("pages/activities.py",), {'title': "Activity Overview"}),
            (("pages/heatmap.py",), {'title': "Strava Heatmap"}),
            (("pages/progress.py",), {'title': "Progress Overview"}),
            (("pages/coastal_path.py",), {'title': "Coastal Path"}),
        ]

        # Assertions
        actual_calls = mock_st.Page.call_args_list
        self.assertEqual(len(actual_calls), len(expected_calls))
        for actual, expected in zip(actual_calls, expected_calls):
            self.assertEqual(actual[0], expected[0])
            self.assertEqual(actual[1], expected[1])

        # Verify st.navigation called with correct pages list
        expected_pages = [
            {'path': "pages/home.py", 'title': "Home"},
            {'path': "pages/activities.py", 'title': "Activity Overview"},
            {'path': "pages/heatmap.py", 'title': "Strava Heatmap"},
            {'path': "pages/progress.py", 'title': "Progress Overview"},
            {'path': "pages/coastal_path.py", 'title': "Coastal Path"},
        ]
        mock_st.navigation.assert_called_once_with(expected_pages)

        # Verify the return value is the mock navigation object
        self.assertEqual(result, mock_nav)
