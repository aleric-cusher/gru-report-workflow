from unittest.mock import patch
from django.db.models.signals import post_save
from django.test import TestCase
from api.tasks import add_agent_workflow, handle_workflow_statuses, logger
from api.models import ContactLeads
from api.signals import on_contact_lead_save
from api.superagi_integration.agent_status import AgentStatus


class TestTasks(TestCase):
    def setUp(self):
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)

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

    @patch("api.tasks.attempt_resume_agent")
    @patch("api.tasks.update_completed_runs")
    @patch("api.tasks.AGIServices")
    def test_handle_workflow_statuses(
        self, mock_agi_services, mock_completed, mock_resume
    ):
        mock_agi_services.return_value.check_run_status.side_effect = [
            AgentStatus.COMPLETED,
            AgentStatus.PAUSED,
        ]
        mock_completed.return_value, mock_resume.return_value = None, None

        ContactLeads.objects.create(
            name="John Doe",
            phone="1234567890",
            company_name="ABC Corp",
            company_website="http://www.abccorp.com",
            industry="Tech",
            goals="Increase efficiency",
            superagi_run_complete=False,
        )
        ContactLeads.objects.create(
            name="Jane Doe",
            phone="9876543210",
            company_name="XYZ Corp",
            company_website="http://www.xyzcorp.com",
            industry="Finance",
            goals="Maximize profits",
            superagi_run_complete=False,
        )

        handle_workflow_statuses()

        mock_agi_services.return_value.check_run_status.assert_called()
        mock_completed.assert_called_once_with(
            [ContactLeads.objects.get(name="John Doe")], mock_agi_services.return_value
        )
        mock_resume.assert_called_once_with(
            [ContactLeads.objects.get(name="Jane Doe")], mock_agi_services.return_value
        )

    @patch("api.tasks.attempt_resume_agent")
    @patch("api.tasks.update_completed_runs")
    @patch("api.tasks.AGIServices")
    def test_handle_workflow_statuses_nothing_to_check(
        self, mock_agi_services, mock_completed, mock_resume
    ):
        handle_workflow_statuses()

        mock_agi_services.assert_not_called()
        mock_completed.assert_not_called()
        mock_resume.assert_not_called()
