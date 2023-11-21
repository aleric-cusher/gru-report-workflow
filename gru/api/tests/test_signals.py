from django.test import TestCase
from django.db.models.signals import post_save
from django.dispatch import Signal
from unittest import mock
from api.models import ContactLeads
from api.signals import on_contact_lead_save


class ContactLeadsSignalTest(TestCase):
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
