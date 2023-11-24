from django.db import IntegrityError
from django.db.models.signals import post_save
from django.test import TestCase
from django.forms import model_to_dict

from api.models import ContactLeads
from api.signals import on_contact_lead_save


class ContactLeadsModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)

    def test_all_fields(self):
        expected_dict = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "message": "Test message",
            "company_name": "Test Company",
            "company_website": "http://www.testcompany.com",
            "industry": "Test Industry",
            "goals": "Test Goals",
            "superagi_run_complete": True,
            "agent_id": 393928,
            "run_id": 123,
            "superagi_resource": "http://www.testcompany.com/color-of-sky.txt",
        }

        ContactLeads.objects.create(**expected_dict)

        contact_lead = model_to_dict(ContactLeads.objects.get(name="John Doe"))

        for each in expected_dict.keys():
            self.assertEqual(contact_lead[each], expected_dict[each])

    def test_required_fields(self):
        expected_dict = {
            "name": "Jane Doe",
            "phone": "1234567890",
            "company_name": "Test Company",
            "company_website": "http://www.testcompany.com",
            "industry": "Test Industry",
            "goals": "Test Goals",
        }

        ContactLeads.objects.create(**expected_dict)

        contact_lead = model_to_dict(ContactLeads.objects.get(name="Jane Doe"))

        for each in expected_dict.keys():
            self.assertEqual(contact_lead[each], expected_dict[each])
