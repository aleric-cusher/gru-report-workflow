import os
from unittest.mock import patch
from django.test import SimpleTestCase
from api.superagi_integration.agi_services import AGIServices
from api.superagi_integration.agi_client_initializer import AGIClientInitializer
from superagi_client import AgentConfig


class MockClient:
    def __init__(self) -> None:
        pass


class TestAGIServices(SimpleTestCase):
    def setUp(self) -> None:
        self.mock_get_client_patcher = patch(
            "api.superagi_integration.agi_client_initializer.AGIClientInitializer.get_client"
        )
        self.mock_get_client = self.mock_get_client_patcher.start()
        self.mock_get_client.return_value = MockClient()

        self.api_key = "test_api_key"
        self.host = "http://test.com"

        self.client_initializer = AGIClientInitializer(self.api_key, self.host)

    def tearDown(self) -> None:
        self.mock_get_client_patcher.stop()

    def test_valid_creation(self):
        services = AGIServices(self.client_initializer)

        self.assertIsInstance(services.client, MockClient)

    def test_invalid_creation(self):
        with self.assertRaises(TypeError):
            services = AGIServices("AGIClientInitializer()")

    def test_private_generate_agent_config_method(self):
        data_dict = {
            "company_name": "Test Company",
            "company_website": "www.testwebsite.com",
            "industry": "Tech",
            "goals": "Testing Goals",
        }

        services = AGIServices(self.client_initializer)
        config = services._generate_agent_config(data_dict)

        self.assertIsInstance(config, AgentConfig)
