# Import dependencies
from backend.functions.authentication import exchange_code_for_token
from unittest.mock import patch, MagicMock
import unittest

class TestExchangeCodeForToken(unittest.TestCase):

    @patch('backend.functions.authentication.requests.post')
    def test_exchange_code_for_token_success(self, mock_post):
        """
        Test to verify exchange code for access token works
        """
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "abc123",
            "token_type": "Bearer"
        }
        mock_post.return_value = mock_response

        # Call function
        result = exchange_code_for_token("client_id", "client_secret", "auth_code")

        # Assert result
        mock_post.assert_called_once_with(
            "https://www.strava.com/api/v3/oauth/token",
            data={
                'client_id': "client_id",
                'client_secret': "client_secret",
                'code': "auth_code",
                'grant_type': 'authorization_code'
            }
        )
        self.assertEqual(result, {"access_token": "abc123", "token_type": "Bearer"})

    @patch('backend.functions.authentication.requests.post')
    def test_exchange_code_for_token_failure(self, mock_post):
        """
        Test behaviour of code to access token failure
        """
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Execute function
        result = exchange_code_for_token("bad_id", "bad_secret", "bad_code")

        # Assert result is none
        self.assertIsNone(result)

    @patch('backend.functions.authentication.requests.post')
    def test_exchange_code_for_token_exception(self, mock_post):
        """
        Test exception handling of code to access token function
        """
        # Mock a network error
        mock_post.side_effect = Exception("Network error")

        # Assert result
        with self.assertRaises(Exception):
            exchange_code_for_token("client_id", "client_secret", "code")
