import os
from unittest.mock import patch
from django.test import SimpleTestCase
from api.superagi_integration.agi_services import AGIServices
from api.superagi_integration.agi_client_initializer import AGIClientInitializer


class MockClient:
    def __init__(self) -> None:
        pass


class TestAGIServices(SimpleTestCase):
    @patch(
        "api.superagi_integration.agi_client_initializer.AGIClientInitializer.get_client"
    )
    def test_valid_creation(self, mock_get_client):
        mock_get_client.return_value = MockClient()

        services = AGIServices(AGIClientInitializer("test_api_key", "http://test.com"))

        self.assertIsInstance(services.client, MockClient)

    def test_invalid_creation(self):
        with self.assertRaises(TypeError):
            services = AGIServices("AGIClientInitializer()")
