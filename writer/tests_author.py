from django.contrib.auth import get_user_model
from django.test import TestCase

from .author import create_author, create_user, get_user

from .models import Author


class UserTestCase(TestCase):
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


class AuthorTestCase(TestCase):

    def setUp(self):
        self.user = create_author(
            # username="johndoe",
            first_name="John",
            last_name="Doe",
            email="john@doe.org")
#         Author.objects.create(user=self.user, name="John Doe")
#         Author.objects.create(user=self.user, name="Jane Smith")

#     def test_get_authors(self):
#         # given
#         authors = Author.objects.create(name="John Doe")
#         authors = Author.objects.create(name="Jane Smith")

#         self.assertEqual(len(authors.get_author()),)

#         # # then
#         # self.assertEqual(result, ["John Doe", "Jane Smith"])
