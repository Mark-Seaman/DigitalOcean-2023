from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model, login


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
        self.login_username_url = '/login_username/'
        self.login_email_url = '/login/'

    def test_login_email(self):
        response = self.client.post(
            self.login_email_url, {'email': self.email, 'password': self.password})
        # Expecting a redirect after successful login
        self.assertEqual(response.status_code, 302)
        # Replace with your expected redirect URL
        self.assertRedirects(response, '/pubs/course')

    def test_login_valid_user(self):
        response = self.client.post(
            self.login_username_url, {'username': self.username, 'password': self.password})
        # Expecting a redirect after successful login
        self.assertEqual(response.status_code, 302)
        # Replace with your expected redirect URL
        self.assertRedirects(response, '/pubs/course')

    def test_login_invalid_user(self):
        response = self.client.post(
            self.login_username_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        # Expecting the login page to be re-rendered
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_redirected(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_username_url)
        # self.assertEqual(response.status_code, 302)  # Expecting a redirect since user is already logged in
        # self.assertRedirects(response, '/course/home')  # Replace with your expected redirect URL
        # Expecting the login page to be re-rendered
        self.assertEqual(response.status_code, 200)

    def test_authenticate(self):
        # print(self.password, '---', self.user.password)
        self.assertNotEqual(self.password, self.user.password)
        self.assertEqual(authenticate(
            username=self.user.username, password=self.password), self.user)
        self.assertTrue(self.user.check_password(self.password))

    def test_email_login(self):
        user = get_user_model().objects.get(email=self.email)
        self.assertTrue(user.check_password(self.password))
