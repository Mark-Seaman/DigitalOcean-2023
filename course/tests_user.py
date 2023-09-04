from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model, login

from course.user import make_user, users


class LoginUnitTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.client = Client()
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'UNC'
        self.user = make_user(email=self.email,
                              name='test user',
                              username=self.username,
                              password=self.password)
        self.login_username_url = '/login_username/'
        self.login_email_url = '/login/'

    def test_username(self):
        u = make_user(email='me@here.us',
                      name='Test User',
                      username=self.username,
                      password=self.password)
        self.assertEqual(len(users()), 1)
        self.assertEqual(u.email, 'me@here.us')
        self.assertEqual(u.last_name, 'User')
        self.assertEqual(u.first_name, 'Test')
        self.assertEqual(len(u.password), 88)

    def test_login_email(self):
        d = {'email': self.email, 'password': self.password}
        response = self.client.post(self.login_email_url, d)
        self.assertEqual(response.status_code, 302)  # redirect after
        self.assertRedirects(response, '/course')   # successful login

    def test_login_valid_user(self):
        d = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_username_url, d)
        self.assertEqual(response.status_code, 302)  # redirect after
        self.assertRedirects(response, '/course')   # successful login

    def test_login_invalid_user(self):
        d = {'username': 'invaliduser', 'password': 'invalidpassword'}
        response = self.client.post(self.login_username_url, d)
        self.assertEqual(response.status_code, 200)  # login page  re-render

    def test_authenticate(self):
        self.assertNotEqual(self.password, self.user.password)
        self.assertEqual(authenticate(
            username=self.user.username, password=self.password), self.user)
        self.assertTrue(self.user.check_password(self.password))

    def test_email_login(self):
        user = get_user_model().objects.get(email=self.email)
        self.assertTrue(user.check_password(self.password))
