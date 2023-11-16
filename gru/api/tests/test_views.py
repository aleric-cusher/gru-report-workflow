import json
from django.forms import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse

from api.models import ContactLeads


class TestContactLeadView(TestCase):
    client = Client()

    def test_valid_contact_lead_view(self):
        request_data = {
            "name": "Joe Doe",
            "email": "joe.doe@example.com",
            "phone": "1234567890",
            "message": "Test message",
            "company_name": "Test Company",
            "company_website": "http://www.testcompany.com",
            "industry": "Test Industry",
            "goals": "Test Goals",
        }

        response = self.client.post(
            reverse("contact-lead"),
            json.dumps(request_data),
            content_type="application/json",
        )
        created_record = model_to_dict(
            ContactLeads.objects.get(
                name=request_data["name"], email=request_data["email"]
            )
        )

        self.assertEquals(response.status_code, 200)
        for each in request_data.keys():
            self.assertEquals(created_record[each], request_data[each])

    def test_method_not_allowed_contact_lead_view(self):
        expected_json = {"error": "Method Not Allowed. Allowed methods are: POST"}

        response = self.client.get(reverse("contact-lead"))

        self.assertEquals(response.status_code, 405)
        self.assertDictEqual(response.json(), expected_json)

    def test_missing_fields_contact_lead_view(self):
        request_data = {
            "name": "Joe Doe",
            "email": "joe.doe@example.com",
            "phone": "1234567890",
            "message": "Test message",
            "company_website": "http://www.testcompany.com",
            "industry": "Test Industry",
            "goals": "Test Goals",
        }
        expected_json = {
            "success": False,
            "error": {"company_name": "This field is required."},
        }

        response = self.client.post(
            reverse("contact-lead"),
            json.dumps(request_data),
            content_type="application/json",
        )

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json(), expected_json)
