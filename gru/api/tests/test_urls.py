from django.test import SimpleTestCase
from django.urls import resolve, reverse
from api import views


class TestUrls(SimpleTestCase):
    def test_contact_lead_url(self):
        url = reverse("contact-lead")
        self.assertEqual(resolve(url).func, views.contact_lead)
