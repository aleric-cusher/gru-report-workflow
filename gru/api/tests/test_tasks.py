from unittest.mock import patch
from django.test import TestCase
from api.tasks import add_agent_workflow, logger
from api.models import ContactLeads


class TestTasks(TestCase):
    @patch("api.tasks.AGIServices")
    def test_add_agent_workflow(self, mock_agi_services):
        mock_agi_services.return_value.create_and_run_agent.return_value = (1, 2)

        model_instance = ContactLeads.objects.create(
            name="John",
            phone="123456789",
            company_name="Example Corp",
            company_website="www.example.com",
            industry="Tech",
            goals="test goals",
        )

        add_agent_workflow(model_instance)

        model_instance.refresh_from_db()
        self.assertEqual(model_instance.agent_id, 1)
        self.assertEqual(model_instance.run_id, 2)
        self.assertFalse(model_instance.superagi_run_complete)

        mock_agi_services.return_value.create_and_run_agent.assert_called_once_with(
            model_instance.get_agi_config_fields()
        )

    @patch("api.tasks.AGIServices")
    @patch("api.tasks.logger")
    def test_add_agent_workflow_exception_handling(
        self, mock_logger, mock_agi_services
    ):
        mock_agi_services.return_value.create_and_run_agent.side_effect = Exception(
            "Test Exception"
        )

        model_instance = ContactLeads.objects.create(
            name="Joe",
            phone="123456789",
            company_name="Example Corp",
            company_website="www.example.com",
            industry="Tech",
            goals="test goals",
        )

        add_agent_workflow(model_instance)

        model_instance.refresh_from_db()

        self.assertIsNone(model_instance.agent_id)
        self.assertIsNone(model_instance.run_id)
        self.assertIsNone(model_instance.superagi_run_complete)

        expected_log_message = "Could not add agent workflow: Test Exception"
        mock_logger.warn.assert_called_once_with(expected_log_message)
