from unittest.mock import MagicMock
from django.test import TestCase
from django.db.models.signals import post_save

from api.models import ContactLeads
from api.signals import on_contact_lead_save
from api.utils import attempt_resume_agent, update_completed_runs, logger


class TestUtils(TestCase):
    def setUp(self):
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)

        ContactLeads.objects.create(
            name="John Doe",
            phone="1234567890",
            company_name="ABC Corp",
            company_website="http://www.abccorp.com",
            industry="Tech",
            goals="Increase efficiency",
            superagi_run_complete=False,
        )

        # Create the second object, skipping optional fields
        ContactLeads.objects.create(
            name="Jane Doe",
            phone="9876543210",
            company_name="XYZ Corp",
            company_website="http://www.xyzcorp.com",
            industry="Finance",
            goals="Maximize profits",
            superagi_run_complete=False,
        )

    def test_update_completed_runs(self):
        records = ContactLeads.objects.all()
        services = MagicMock()
        services.get_resource_url.return_value = "http://test.com/resource_file.txt"

        update_completed_runs(records, services)

        for each in records:
            each.refresh_from_db()
            self.assertEqual(
                each.superagi_resource, "http://test.com/resource_file.txt"
            )
            self.assertTrue(each.superagi_run_complete)

        services.get_resource_url.assert_called()

    def test_update_completed_runs_empty_records(self):
        services = MagicMock()
        services.get_resource_url.return_value = "http://test.com/resource_file.txt"

        try:
            update_completed_runs([], services)
        except Exception as e:
            self.fail("Exception: " + str(e))

        services.assert_not_called()

    def test_update_completed_runs_error(self):
        records = ContactLeads.objects.all()
        services = MagicMock()
        services.get_resource_url.side_effect = Exception("Test exception")

        with self.assertLogs(logger, "WARNING") as log_capture:
            update_completed_runs(records, services)

        for record in records:
            self.assertIn(
                f"WARNING:api.utils:Exception occured while updating agent run status and resource url for {record}: Test exception",
                log_capture.output,
            )

    def test_attempt_resume_agent_successful(self):
        records = ContactLeads.objects.all()
        services = MagicMock()
        services.resume_agent.return_value = True

        with self.assertLogs(logger, "INFO") as log_capture:
            attempt_resume_agent(records, services)

        for record in records:
            self.assertIn(
                f"INFO:api.utils:Resumed agent run for {record}", log_capture.output
            )
        services.resume_agent.assert_called()

    def test_attempt_resume_agent_unsuccessful(self):
        records = ContactLeads.objects.all()
        services = MagicMock()
        services.resume_agent.return_value = False

        with self.assertLogs(logger, "WARNING") as log_capture:
            attempt_resume_agent(records, services)

        for record in records:
            self.assertIn(
                f"WARNING:api.utils:Could not resume agent run for {record}",
                log_capture.output,
            )
        services.resume_agent.assert_called()

    def test_attempt_resume_agent_empty_records(self):
        services = MagicMock()
        services.resume_agent.return_value = True

        try:
            attempt_resume_agent([], services)
        except Exception as e:
            self.fail("Exception: " + str(e))

        services.assert_not_called()

    def test_attempt_resume_agent_error(self):
        records = ContactLeads.objects.all()
        services = MagicMock()
        services.resume_agent.side_effect = Exception("Test exception")

        with self.assertLogs(logger, "WARNING") as log_capture:
            attempt_resume_agent(records, services)

        for record in records:
            self.assertIn(
                f"WARNING:api.utils:Exception occured while resuming agent run for {record}: Test exception",
                log_capture.output,
            )
