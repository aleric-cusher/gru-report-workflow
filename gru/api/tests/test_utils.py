from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.db.models.signals import post_save

from api.models import ContactLeads
from api.signals import on_contact_lead_save
from api.utils import (
    attempt_resume_agent,
    download_file_from_s3,
    update_completed_runs,
    logger,
)


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

    @patch("api.utils.boto3")
    def test_download_file_from_s3(self, mock_boto):
        test_url = "https://awsforagi.s3.amazonaws.com/public_resources/run_id57/sky_color_explanation.txt"
        test_local_path = "test_path"
        test_key_id = "test_key_id"
        test_key = "test-xyzabc"
        bucket = "awsforagi"
        url_key = "public_resources/run_id57/sky_color_explanation.txt"

        mock_s3 = MagicMock()
        mock_s3.download_file.return_value = None
        mock_boto.client.return_value = mock_s3

        result = download_file_from_s3(test_url, test_local_path, test_key_id, test_key)

        self.assertTrue(result)
        mock_boto.client.assert_called_once_with(
            "s3", aws_access_key_id=test_key_id, aws_secret_access_key=test_key
        )
        mock_s3.download_file.assert_called_once_with(bucket, url_key, test_local_path)

    @patch("api.utils.boto3")
    def test_download_file_from_s3_error(self, mock_boto):
        test_url = "https://awsforagi.s3.amazonaws.com/public_resources/run_id57/sky_color_explanation.txt"
        test_local_path = "test_path"
        test_key_id = "test_key_id"
        test_key = "test-xyzabc"

        mock_s3 = MagicMock()
        mock_s3.download_file.side_effect = Exception("Test exception")
        mock_boto.client.return_value = mock_s3

        with self.assertLogs(logger, "ERROR") as log_capture:
            result = download_file_from_s3(
                test_url, test_local_path, test_key_id, test_key
            )

        self.assertFalse(result)
        self.assertIn(
            "ERROR:api.utils:Exception occured while downloading file form s3: Test exception",
            log_capture.output,
        )
