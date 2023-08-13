from django.test import TestCase
from .models import SWUser


class CustomUserModelTest(TestCase):

    def setUp(self):
        # Set up test data
        self.user = SWUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_superuser_creation(self):
        admin_user = SWUser.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_authentication(self):
        authenticated_user = SWUser.objects.get(email='test@example.com')
        self.assertTrue(authenticated_user.check_password('testpassword'))

    def test_invalid_user_authentication(self):
        wrong_password_user = SWUser.objects.get(email='test@example.com')
        self.assertFalse(wrong_password_user.check_password('wrongpassword'))

    # def test_email_uniqueness(self):
    #     with self.assertRaises(ValueError):
    #         SWUser.objects.create_user(
    #             username='anotheruser',
    #             email='test@example.com',  # Repeating the same email
    #             password='anotherpassword'
    #         )
