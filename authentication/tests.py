from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()


class AuthenticationByEmailOrUsernameTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'bob'
        self.email = 'bob@example.com'
        self.password = 'pass12345'
        User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_token_with_username(self):
        resp = self.client.post('/api/v1/authentication/token/', {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_token_with_email_field(self):
        resp = self.client.post('/api/v1/authentication/token/', {'email': self.email, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIn('access', resp.data)

    def test_token_with_username_as_email_string(self):
        # sending the email in the 'username' field should also work
        resp = self.client.post('/api/v1/authentication/token/', {'username': self.email, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIn('access', resp.data)
