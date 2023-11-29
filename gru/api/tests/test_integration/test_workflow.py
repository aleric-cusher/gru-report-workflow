import json
from unittest.mock import patch
from django.forms import model_to_dict
from django.test import TestCase, Client
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from api.signals import on_contact_lead_save, on_superagi_run_complete_update
from api.models import ContactLeads


class TestWorkflows(TestCase):
    def setUp(self):
        pre_save.connect(on_superagi_run_complete_update, sender=ContactLeads)
        post_save.connect(on_contact_lead_save, sender=ContactLeads)

    def tearDown(self) -> None:
        pre_save.disconnect(on_superagi_run_complete_update, sender=ContactLeads)
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)

    @patch("api.signals.add_agent_workflow.delay")
    def test_view_to_celery_add_workflow(self, mock_add_agent_workflow):
        data = {
            "name": "test",
            "email": "test@test.com",
            "phone": "1234567890",
            "message": "message",
            "industry": "Furniture",
            "company_website": "https://www.companywebsite.com",
            "facebook": "",
            "instagram": "",
            "linkedin": "",
            "goals": "goals",
            "company_name": "Company Name",
        }

        expected_response = {
            "success": True,
            "message": "Form received, We will get back to you shortly!",
        }

        client = Client()
        mock_add_agent_workflow.return_value = None

        response = client.post(
            reverse("contact-lead"),
            json.dumps(data),
            content_type="application/json",
        )

        contact_lead = ContactLeads.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_response)
        mock_add_agent_workflow.assert_called_once_with(contact_lead.pk)

        keys_to_check = [
            "name",
            "email",
            "phone",
            "message",
            "industry",
            "company_website",
            "goals",
            "company_name",
        ]
        model_dict = model_to_dict(contact_lead, keys_to_check)
        for each in model_dict.keys():
            self.assertEqual(model_dict[each], data[each])
