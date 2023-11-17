from api.superagi_integration.agi_client_initializer import AGIClientInitializer
from django.test import SimpleTestCase


class TestAGIClientInitializer(SimpleTestCase):
    def test_valid_creation(self):
        initializer = AGIClientInitializer(
            "abcdefghijklmnopqrstuvwxyz", "http://127.0.0.1:3000"
        )

        self.assertEqual(initializer.api_key, "abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(initializer.host, "http://127.0.0.1:3000")
        self.assertEqual(initializer.client, None)

    def test_invalid_creation(self):
        with self.assertRaises(TypeError):
            initializer = AGIClientInitializer(1234567890, "http://127.0.0.1:3000")

        with self.assertRaises(TypeError):
            initializer = AGIClientInitializer("abcdefghijklmnopqrstuvwxyz", 1234567890)

        with self.assertRaises(TypeError):
            initializer = AGIClientInitializer(1234567890, 1234567890)
