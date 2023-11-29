from unittest.mock import MagicMock, patch
from django.db.models.signals import post_save, pre_save
from django.test import TestCase
from api.tasks import (
    add_agent_workflow,
    handle_workflow_statuses,
    logger,
    process_and_email_report,
)
from api.models import ContactLeads
from api.signals import on_contact_lead_save, on_superagi_run_complete_update
from api.superagi_integration.agent_status import AgentStatus


class TestTasks(TestCase):
    def setUp(self):
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)
        pre_save.disconnect(on_superagi_run_complete_update, sender=ContactLeads)

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

        add_agent_workflow(model_instance.pk)

        model_instance.refresh_from_db()
        self.assertEqual(model_instance.agent_id, 1)
        self.assertEqual(model_instance.run_id, 2)
        self.assertFalse(model_instance.superagi_run_complete)

        mock_agi_services.return_value.create_and_run_agent.assert_called_once_with(
            model_instance.get_agi_config_fields()
        )

    @patch("api.tasks.AGIServices")
    def test_add_agent_workflow_exception_handling(self, mock_agi_services):
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

        with self.assertLogs(logger, "ERROR") as log_capture:
            add_agent_workflow(model_instance.pk)

        model_instance.refresh_from_db()

        self.assertIsNone(model_instance.agent_id)
        self.assertIsNone(model_instance.run_id)
        self.assertIsNone(model_instance.superagi_run_complete)

        self.assertIn(
            f"ERROR:api.tasks:Could not add agent workflow for {model_instance}: Test Exception",
            log_capture.output,
        )

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

    @patch("api.tasks.read_file_from_s3")
    @patch("api.tasks.generate_pdf")
    @patch("api.tasks.send_email_with_report")
    def test_process_and_email_report(
        self, mock_send_email, mock_generate_pdf, mock_read_from_s3
    ):
        mock_read_from_s3.return_value = '{"key": "value"}'
        mock_generate_pdf.return_value = b"pdf_content"
        mock_send_email.return_value = True

        record = ContactLeads.objects.create(
            superagi_resource="http://test.com/test.txt"
        )

        result = process_and_email_report(record.pk)

        self.assertTrue(result)
        mock_read_from_s3.assert_called_once_with("http://test.com/test.txt")
        mock_generate_pdf.assert_called_once_with({"key": "value"})
        mock_send_email.assert_called_once_with(record, b"pdf_content")

    @patch("api.tasks.read_file_from_s3")
    @patch("api.tasks.generate_pdf")
    @patch("api.tasks.send_email_with_report")
    def test_process_and_email_report_file_not_found(
        self, mock_send_email, mock_generate_pdf, mock_read_from_s3
    ):
        mock_read_from_s3.return_value = None

        record = ContactLeads.objects.create(
            superagi_resource="http://test.com/test.txt"
        )

        result = process_and_email_report(record.pk)

        self.assertFalse(result)
        mock_read_from_s3.assert_called_once_with("http://test.com/test.txt")
        mock_generate_pdf.assert_not_called()
        mock_send_email.assert_not_called()
