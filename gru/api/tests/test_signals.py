from django.test import TestCase
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal
from unittest import mock
from api.models import ContactLeads
from api.signals import on_contact_lead_save, on_superagi_run_complete_update


class ContactLeadsSignalTest(TestCase):
    def setUp(self) -> None:
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)
        pre_save.disconnect(on_superagi_run_complete_update, sender=ContactLeads)

    def test_on_contact_lead_save_signal(self):
        contact_lead_instance = ContactLeads.objects.create(name="Test Contact Lead")

        with mock.patch("api.signals.add_agent_workflow") as mock_add_agent_workflow:
            with mock.patch(
                "api.signals.add_agent_workflow.delay", mock_add_agent_workflow
            ):
                # Trigger the post_save signal manually
                post_save.connect(on_contact_lead_save, sender=ContactLeads)
                post_save.send(
                    sender=ContactLeads, instance=contact_lead_instance, created=True
                )

        # Disconnect the signal to avoid interference with other tests
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)
        mock_add_agent_workflow.assert_called_once_with(contact_lead_instance)

    def test_on_superagi_run_complete_update(self):
        contact_lead_instance = ContactLeads.objects.create(name="Test Contact Lead")

        with mock.patch(
            "api.signals.process_and_email_report"
        ) as mock_process_and_email_report:
            with mock.patch(
                "api.signals.process_and_email_report.delay",
                mock_process_and_email_report,
            ):
                pre_save.connect(on_superagi_run_complete_update, sender=ContactLeads)
                contact_lead_instance.superagi_run_complete = True
                contact_lead_instance.superagi_resource = "https://testresource.com"
                contact_lead_instance.save()

        pre_save.disconnect(on_superagi_run_complete_update, sender=ContactLeads)
        mock_process_and_email_report.assert_called_once_with(contact_lead_instance)
