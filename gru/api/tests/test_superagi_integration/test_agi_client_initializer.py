from unittest.mock import MagicMock, patch
from api.superagi_integration.agi_client_initializer import AGIClientInitializer
from django.test import SimpleTestCase


class TestAGIClientInitializer(SimpleTestCase):
    def test_valid_creation(self):
        api_key = "test_api_key"
        host = "http://test.com"
        initializer = AGIClientInitializer(api_key, host)

        self.assertEqual(initializer.api_key, api_key)
        self.assertEqual(initializer.host, host)
        self.assertEqual(initializer.client, None)

    def test_invalid_creation(self):
        with self.assertRaises(TypeError):
            initializer = AGIClientInitializer(1234567890, "http://test.com")

        with self.assertRaises(TypeError):
            initializer = AGIClientInitializer("test_api_key", 1234567890)

        with self.assertRaises(TypeError):
            initializer = AGIClientInitializer(1234567890, 1234567890)

    @patch("api.superagi_integration.agi_client_initializer.Client")
    def test_get_client(self, mock_client):
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        api_key = "test_api_key"
        host = "http://test.com"
        initializer = AGIClientInitializer(api_key=api_key, host=host)
        client = initializer.get_client()

        mock_client.assert_called_once_with(api_key, host)
        self.assertIs(client, mock_client_instance)
