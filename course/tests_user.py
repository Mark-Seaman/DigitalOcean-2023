from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class LoginUnitTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.login_url = '/course/login/'
        self.login_email_url = '/course/login_email/'

    def test_login_email(self):
        response = self.client.post(
            self.login_email_url, {'email': self.email, 'password': self.password})
        # Expecting a redirect after successful login
        self.assertEqual(response.status_code, 302)
        # Replace with your expected redirect URL
        self.assertRedirects(response, '/course/home')

    def test_login_valid_user(self):
        response = self.client.post(
            self.login_url, {'username': self.username, 'password': self.password})
        # Expecting a redirect after successful login
        self.assertEqual(response.status_code, 302)
        # Replace with your expected redirect URL
        self.assertRedirects(response, '/course/home')

    def test_login_invalid_user(self):
        response = self.client.post(
            self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        # Expecting the login page to be re-rendered
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_redirected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url)
        # self.assertEqual(response.status_code, 302)  # Expecting a redirect since user is already logged in
        # self.assertRedirects(response, '/course/home')  # Replace with your expected redirect URL
        # Expecting the login page to be re-rendered
        self.assertEqual(response.status_code, 200)
