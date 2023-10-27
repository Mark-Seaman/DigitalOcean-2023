from django.contrib.auth import get_user_model
from django.test import TestCase

from .author import authors, create_author, create_user, get_user

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

    def test_create_author(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertEqual(author.user.username, "johndoe")
        self.assertEqual(author.name, "John Doe")

    def test_existing_user(self):
        create_user(username="janesmith")
        author = create_author(username="janesmith",
                               first_name="John", last_name="Doe")
        self.assertEqual(author.user.username, "janesmith")
        self.assertEqual(author.name, "John Doe")

    def test_existing_author(self):
        author = create_author(first_name="john", last_name="doe")
        author = create_author(username="johndoe",
                               first_name="jane", last_name="doe")
        self.assertEqual(author.user.username, "johndoe")
        self.assertEqual(author.user.first_name, "jane")
        self.assertEqual(len(get_user_model().objects.all()), 1)

    def test_no_name(self):
        with self.assertRaises(AssertionError):
            create_author()

    def test_no_username(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertEqual(author.user.username, "johndoe")
        self.assertEqual(author.user.first_name, "John")

    def test_no_email(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertEqual(author.user.email, "johndoe@shrinking-world.com")

    def test_no_password(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertNotEqual(author.user.password, "password")
        self.assertTrue(author.user.check_password("password"))

    def test_reset_password(self):
        author = create_author(first_name="John", last_name="Doe")
        author.user.set_password("newpassword")
        self.assertTrue(author.user.check_password("newpassword"))

    def test_get_authors(self):
        create_author(first_name="John", last_name="Doe")
        create_author(first_name="Jane", last_name="Smith")
        self.assertEqual(len(authors()), 2)
        self.assertEqual(len(authors(user__first_name='Jane')), 1)

    def test_get_author(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertEqual(get_user("johndoe").author, author)
        self.assertEqual(get_user("johndoe").author.name, "John Doe")
        self.assertEqual(get_user("johndoe").author.user.username, "johndoe")
        self.assertEqual(get_user("johndoe").author.user.email,
                         "johndoe@shrinking-world.com")

    def test_author_str(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertEqual(str(author), "John Doe")

    def test_author_sort(self):
        create_author(first_name="John", last_name="Doe")
        create_author(first_name="John", last_name="Smith")
        create_author(first_name="Jane", last_name="Smith")
        create_author(first_name="Abe", last_name="Lincoln")
        create_author(first_name="George", last_name="Washington")
        self.assertEqual(str(authors()[0]), "John Doe")
        self.assertEqual(str(authors()[1]), "Abe Lincoln")
        self.assertEqual(str(authors()[2]), "Jane Smith")
        self.assertEqual(str(authors()[3]), "John Smith")
        self.assertEqual(str(authors()[4]), "George Washington")

    def test_author_bio(self):
        author = create_author(first_name="John", last_name="Doe")
        self.assertEqual(author.bio, "")
        author.bio = "This is my bio"
        author.save()
        self.assertEqual(author.bio, "This is my bio")
