from io import BytesIO
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from django.db.models.signals import post_save
from django.core import mail
from django.core.files.base import ContentFile

from api.models import ContactLeads
from api.signals import on_contact_lead_save
from api.utils import (
    attempt_resume_agent,
    download_file_from_s3,
    generate_pdf,
    read_file_from_s3,
    send_email_with_report,
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

        update_completed_runs([], services)

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

        attempt_resume_agent([], services)

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

    @patch("api.utils.boto3")
    def test_read_file_from_s3(self, mock_boto):
        test_url = "https://awsforagi.s3.amazonaws.com/public_resources/run_id57/sky_color_explanation.txt"
        test_key_id = "test_key_id"
        test_key = "test-xyzabc"
        expected_result = b'{"Content": "Test Content"}'
        bucket = "awsforagi"
        url_key = "public_resources/run_id57/sky_color_explanation.txt"

        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=expected_result))
        }
        mock_boto.client.return_value = mock_s3

        result = read_file_from_s3(test_url, test_key_id, test_key)

        self.assertEqual(result, expected_result.decode())
        mock_boto.client.assert_called_once_with(
            "s3", aws_access_key_id=test_key_id, aws_secret_access_key=test_key
        )
        mock_s3.get_object.assert_called_once_with(Bucket=bucket, Key=url_key)

    @patch("api.utils.boto3")
    def test_read_file_from_s3_error(self, mock_boto):
        test_url = "https://awsforagi.s3.amazonaws.com/public_resources/run_id57/sky_color_explanation.txt"
        test_key_id = "test_key_id"
        test_key = "test-xyzabc"
        expected_result = b'{"Content": "Test Content"}'
        bucket = "awsforagi"
        url_key = "public_resources/run_id57/sky_color_explanation.txt"

        mock_s3 = MagicMock()
        mock_s3.get_object.side_effect = Exception("Test exception")
        mock_boto.client.return_value = mock_s3

        with self.assertLogs(logger, "ERROR") as log_capture:
            result = read_file_from_s3(test_url, test_key_id, test_key)

        self.assertIsNone(result)
        self.assertIn(
            "ERROR:api.utils:Error reading file from S3: Test exception",
            log_capture.output,
        )
        mock_boto.client.assert_called_once_with(
            "s3", aws_access_key_id=test_key_id, aws_secret_access_key=test_key
        )
        mock_s3.get_object.assert_called_once_with(Bucket=bucket, Key=url_key)

    def test_generate_pdf(self):
        data = {
            "title": "Office Smart Report",
            "headings": [
                {
                    "heading": "Company Overview",
                    "content": "Office Smart is a company that offers a wide range of office supplies and solutions to businesses of all sizes and individuals with home offices.",
                },
                {
                    "heading": "Market Analysis",
                    "content": "The office supplies market is a competitive one, with several key players. Office Smart has a significant market potential due to its broad target market and diverse product offerings.",
                },
            ],
        }

        pdf_buffer = generate_pdf(data)

        self.assertIsInstance(pdf_buffer, BytesIO)
        self.assertNotEqual(pdf_buffer.getvalue(), b"")


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class EmailUtilityTest(TestCase):
    def setUp(self):
        # Create a test ContactLeads record
        self.test_record = ContactLeads.objects.create(
            company_name="Test Company",
            name="Test User",
            email="test@example.com"
            # Add other necessary fields for your ContactLeads model
        )

    def test_send_email_with_report(self):
        # Create an in-memory PDF file
        pdf_content = b"Mock PDF content"
        pdf_file = ContentFile(pdf_content)

        with self.assertLogs(logger, "INFO") as log_capture:
            send_email_with_report(self.test_record, pdf_file)

        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the subject, recipient, and attachment of the sent email
        sent_email = mail.outbox[0]
        expected_subject = f"{self.test_record.company_name} Analysis Report"
        self.assertEqual(sent_email.subject, expected_subject)
        self.assertEqual(
            sent_email.body,
            f"Dear {self.test_record.name},\n\nYour AI-generated report is ready and attached to this email. If you have any questions or need further assistance, please feel free to reach out. We're here to help!\n\nEnjoy your day!\n\nBest Regards,\nGRU\n",
        )
        self.assertEqual(sent_email.to, [self.test_record.email])

        # Check if the attachment is present
        self.assertEqual(len(sent_email.attachments), 1)
        attachment = sent_email.attachments[0]
        filename, attachment_content, mimetype = attachment
        self.assertEqual(filename, f"{self.test_record.company_name} Report.pdf")
        self.assertEqual(attachment_content, pdf_content)
        self.assertEqual(mimetype, "application/pdf")

        self.assertIn(
            f"INFO:api.utils:Email with report for {self.test_record} sent successfully to {self.test_record.email}",
            log_capture.output,
        )

    @patch("api.utils.EmailMessage.send")
    def test_send_email_with_report_exception(self, mock_send):
        mock_send.side_effect = Exception("Test exception")

        pdf_content = b"Mock PDF content"
        pdf_file = ContentFile(pdf_content)

        with self.assertLogs(logger, "ERROR") as log_capture:
            send_email_with_report(self.test_record, pdf_file)

        self.assertIn(
            f"ERROR:api.utils:Failed to send email with report to {self.test_record}. Error: Test exception",
            log_capture.output,
        )
