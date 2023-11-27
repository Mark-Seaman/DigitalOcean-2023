from django.contrib.auth import get_user_model
from django.test import TestCase

from publish.note import create_moderators

from .author import create_user, get_user


class UserDataTest(TestCase):
    def setUp(self):
        create_user(username="johndoe", email="john@shrinking-world.com",
                    first_name="John", last_name="Doe")
        create_user(username="janesmith")

    def test_get_users(self):
        self.assertEqual(len(get_user_model().objects.all()), 2)

    def test_get_user(self):
        john = get_user("johndoe")
        jane = get_user("janesmith")
        self.assertEqual(john.username, "johndoe")
        self.assertEqual(jane.username, "janesmith")
        self.assertEqual(john.email, "john@shrinking-world.com")
        self.assertEqual(jane.email, "janesmith@shrinking-world.com")
        self.assertEqual(jane.first_name, "First name")

    def test_create_user(self):
        self.assertEqual(get_user("janesmith").first_name, "First name")

    def test_duplicate_username(self):
        create_user(username="johndoe", email="x@y.us")
        self.assertEqual(len(get_user_model().objects.all()), 2)

    def test_password(self):
        john = get_user("johndoe")
        self.assertNotEqual(john.password, "password")
        self.assertTrue(john.check_password("password"))

    def test_no_username(self):
        with self.assertRaises(AssertionError):
            create_user()

    def test_moderator(self):
        create_moderators(self)
