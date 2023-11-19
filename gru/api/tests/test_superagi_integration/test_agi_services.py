import os
from unittest.mock import MagicMock, patch
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
        self.mock_client_instance = MagicMock()
        self.mock_get_client.return_value = self.mock_client_instance

        self.api_key = "test_api_key"
        self.host = "http://test.com"

        self.client_initializer = AGIClientInitializer(self.api_key, self.host)
        self.services = AGIServices(self.client_initializer)

    def tearDown(self) -> None:
        self.mock_get_client_patcher.stop()

    @patch(
        "api.superagi_integration.agi_client_initializer.AGIClientInitializer.get_client"
    )
    def test_valid_creation(self, mock_get_client):
        mock_get_client.return_value = MockClient()
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

        config = self.services._generate_agent_config(data_dict)

        self.assertIsInstance(config, AgentConfig)

    def test_create_agent_method(self):
        self.mock_client_instance.create_agent.return_value = {"agent_id": 1}
        data_dict = {
            "company_name": "Test Company",
            "company_website": "www.testwebsite.com",
            "industry": "Tech",
            "goals": "Testing Goals",
        }
        agent_id = self.services.create_agent(data_dict)

        self.assertEqual(agent_id, 1)
        self.mock_client_instance.create_agent.assert_called_once()

    def test_run_agent_method(self):
        agent_id = 1
        self.mock_client_instance.create_agent_run.return_value = {"run_id": 2}
        run_id = self.services.run_agent(agent_id)

        self.assertEqual(run_id, 2)
        self.mock_client_instance.create_agent_run.assert_called_once()

    def test_create_and_run_agent_method(self):
        data_dict = {
            "company_name": "Test Company",
            "company_website": "www.testwebsite.com",
            "industry": "Tech",
            "goals": "Testing Goals",
        }

        self.mock_client_instance.create_agent.return_value = {"agent_id": 1}
        self.mock_client_instance.create_agent_run.return_value = {"run_id": 2}

        agent_id, run_id = self.services.create_and_run_agent(data_dict)

        self.assertEqual(agent_id, 1)
        self.assertEqual(run_id, 2)

        self.mock_client_instance.create_agent.assert_called_once()
        self.mock_client_instance.create_agent_run.assert_called_once()

    def test_pause_agent_method(self):
        self.mock_client_instance.pause_agent.return_value = {"result": "success"}
        paused = self.services.pause_agent(1, 2)

        self.assertEqual(paused, True)
        self.mock_client_instance.pause_agent.assert_called_once()

    def test_resume_agent_method(self):
        self.mock_client_instance.resume_agent.return_value = {"result": "success"}
        resumed = self.services.resume_agent(1, 2)

        self.assertEqual(resumed, True)
        self.mock_client_instance.resume_agent.assert_called_once()
