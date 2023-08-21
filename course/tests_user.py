from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class LoginUnitTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password
        )
        self.login_url = '/login/'  # Replace with your actual login URL

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful login
        self.assertRedirects(response, '/home/')  # Replace with your expected redirect URL

    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)  # Expecting the login page to be re-rendered

    def test_authenticated_user_redirected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect since user is already logged in
        self.assertRedirects(response, '/home/')  # Replace with your expected redirect URL
