from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import SWUser


# class LoginViewTest(TestCase):

#     def setUp(self):
#         self.username = 'testuser'
#         self.password = 'testpassword'
#         self.user = SWUser.objects.create_user(
#             username=self.username,
#             email='testuser@shrinking-world.com',
#             password=self.password
#         )
#         # Assuming you've named your login URL as 'login'
#         self.login_url = reverse('login')

#     def test_login_valid_user(self):
#         response = self.client.post(
#             self.login_url, {'username': self.username, 'password': self.password})
#         # Expecting a redirect after successful login
#         self.assertEqual(response.status_code, 302)
#         # Replace 'home' with your desired redirect URL
#         self.assertRedirects(response, reverse('home'))

#     def test_login_invalid_user(self):
#         response = self.client.post(
#             self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
#         # Expecting the login page to be re-rendered
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Invalid credentials. Please try again.")

#     def test_login_empty_fields(self):
#         response = self.client.post(
#             self.login_url, {'username': '', 'password': ''})
#         # Expecting the login page to be re-rendered
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "This field is required.")

#     def test_authenticated_user_redirected(self):
#         self.client.login(username=self.username, password=self.password)
#         response = self.client.get(self.login_url)
#         # Expecting a redirect since user is already logged in
#         self.assertEqual(response.status_code, 302)

#     def test_login_page_renders(self):
#         response = self.client.get(self.login_url)
#         # Expecting successful rendering of the login page
#         self.assertEqual(response.status_code, 200)
#         # Adjust the template path as needed
#         self.assertTemplateUsed(response, 'login.html')


class LoginViewTest(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = SWUser.objects.create_user(
            username='testuser',
            email=self.email,
            password=self.password
        )
        # Assuming you've named your login URL as 'login'
        self.login_url = reverse('login')

    # def test_login_valid_user(self):
    #     response = self.client.post(
    #         self.login_url, {'email': self.email, 'password': self.password})
    #     # Expecting a redirect after successful login
    #     self.assertEqual(response.status_code, 302)
    #     # Replace 'home' with your desired redirect URL
    #     self.assertRedirects(response, reverse('home'))

    # def test_login_invalid_user(self):
    #     response = self.client.post(
    #         self.login_url, {'email': 'invalid@example.com', 'password': 'invalidpassword'})
    #     # Expecting the login page to be re-rendered
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertContains(response, "Invalid credentials. Please try again.")

    # def test_login_empty_fields(self):
    #     response = self.client.post(
    #         self.login_url, {'email': '', 'password': ''})
    #     # Expecting the login page to be re-rendered
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertContains(response, "This field is required.")

    # def test_authenticated_user_redirected(self):
    #     # self.client.login(email=self.email, password=self.password)
    #     # response = self.client.get(self.login_url)
    #     # # Expecting a redirect since user is already logged in
    #     # self.assertEqual(response.status_code, 302)

    # def test_login_page_renders(self):
    #     response = self.client.get(self.login_url)
    #     # Expecting successful rendering of the login page
    #     self.assertEqual(response.status_code, 200)
    #     # Adjust the template path as needed
    #     self.assertTemplateUsed(response, 'login.html')
