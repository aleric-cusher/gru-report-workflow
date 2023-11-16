from django.test import TestCase
from api.models import ContactLeads


class ContactLeadsModelTest(TestCase):
    def test_all_fields(self):
        ContactLeads.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone="1234567890",
            message="Test message",
            company_name="Test Company",
            company_website="http://www.testcompany.com",
            industry="Test Industry",
            goals="Test Goals",
        )

        contact_lead = ContactLeads.objects.get(name="John Doe")

        self.assertEqual(contact_lead.name, "John Doe")
        self.assertEqual(contact_lead.email, "john.doe@example.com")
        self.assertEqual(contact_lead.phone, "1234567890")
        self.assertEqual(contact_lead.message, "Test message")
        self.assertEqual(contact_lead.company_name, "Test Company")
        self.assertEqual(contact_lead.company_website, "http://www.testcompany.com")
        self.assertEqual(contact_lead.industry, "Test Industry")
        self.assertEqual(contact_lead.goals, "Test Goals")

    def test_required_fields(self):
        # Test creating a ContactLeads instance with only required fields
        ContactLeads.objects.create(
            name="Jane Doe",
            phone="1234567890",
            company_name="Test Company",
            company_website="http://www.testcompany.com",
            industry="Test Industry",
            goals="Test Goals",
        )

        contact_lead = ContactLeads.objects.get(name="Jane Doe")

        self.assertEqual(contact_lead.name, "Jane Doe")
        self.assertIsNone(contact_lead.email)
        self.assertEqual(contact_lead.phone, "1234567890")
        self.assertIsNone(contact_lead.message)
        self.assertEqual(contact_lead.company_name, "Test Company")
        self.assertEqual(contact_lead.company_website, "http://www.testcompany.com")
        self.assertEqual(contact_lead.industry, "Test Industry")
        self.assertEqual(contact_lead.goals, "Test Goals")
