from django.contrib.auth.models import User 
from django.test import TestCase
from django.urls import reverse

from .models import YourModel
from .forms import YourModelForm


class YourModelUpdateViewTest(TestCase):

    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.instance = YourModel.objects.create(name='Test Name', description='Test Description')
        self.url = reverse('yourmodel-update', args=[self.instance.pk])
        self.data = {
            'name': 'Updated Name',
            'description': 'Updated Description',
        }



    def test_update_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'yourapp/yourmodel_form.html')  # Replace with your actual template name

    def test_update_view_updates_object(self):
        response = self.client.post(self.url, data=self.data)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, 'Updated Name')
        self.assertEqual(self.instance.description, 'Updated Description')

    def test_update_view_form_validation(self):
        # Test invalid form data
        invalid_data = {
            'name': '',  # Required field, should be invalid
            'description': 'Updated Description',
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_update_view_redirects_after_successful_update(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
        self.assertRedirects(response, reverse('yourmodel-detail', args=[self.instance.pk]))  # Replace with your detail view URL name

