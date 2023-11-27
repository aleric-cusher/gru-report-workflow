from django.db.models.signals import post_save, pre_save
from django.test import TestCase

from api.forms import ContactLeadsForm
from api.signals import on_contact_lead_save, on_superagi_run_complete_update
from api.models import ContactLeads


class ContactLeadsFormTest(TestCase):
    def setUp(self):
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)
        pre_save.disconnect(on_superagi_run_complete_update, sender=ContactLeads)

    def test_valid_form(self):
        form_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "message": "Test message",
            "company_name": "Test Company",
            "company_website": "http://www.testcompany.com",
            "industry": "Test Industry",
            "goals": "Test Goals",
        }

        form = ContactLeadsForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            # Missing required field "company_website"
            "name": "John Doe",
            "phone": "1234567890",
            "company_name": "Test Company",
            "industry": "Test Industry",
            "goals": "Test Goals",
        }

        form = ContactLeadsForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("company_website", form.errors.keys())
        self.assertEqual(form.errors["company_website"], ["This field is required."])

    def test_optional_fields(self):
        form_data = {
            "name": "John Doe",
            "phone": "1234567890",
            "company_name": "Test Company",
            "company_website": "http://www.testcompany.com",
            "industry": "Test Industry",
            "goals": "Test Goals",
        }

        form = ContactLeadsForm(data=form_data)

        self.assertTrue(form.is_valid())
