from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from writer.views import AuthorUpdateView

from .author import authors, create_author, create_user, get_user

from .models import Author


class AuthorDataTest(TestCase):

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
        self.assertEqual(author.bio, None)
        author.bio = "This is my bio"
        author.save()
        self.assertEqual(author.bio, "This is my bio")


class AuthorViewTest(TestCase):
    def setUp(self):
        self.author = create_author(first_name="John", last_name="Doe")

    def test_list_view(self):
        response = self.client.get('/writer/author/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertTemplateUsed(response, 'list.html')
        self.assertTemplateUsed(response, 'publish_theme.html')

    def test_detail_view(self):
        response = self.client.get('/writer/author/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertTemplateUsed(response, 'detail.html')

    def test_add_without_login(self):
        response = self.client.get('/writer/author/add')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/writer/author/add')

    def test_add_get(self):
        self.assertTrue(self.client.login(
            username='johndoe', password='password'))
        response = self.client.get('/writer/author/add')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Save Record")
        self.assertTemplateUsed(response, 'edit.html')

    def test_add_post(self):
        user = create_user(username="mds", email="mark.seaman@shrinking-world.com",
                           first_name="Mark", last_name="Seaman")
        self.assertTrue(self.client.login(username="mds", password="password"))
        data = dict(username=user.username, name='Mark Seaman')
        response = self.client.post('/writer/author/add', data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/writer/author/2')
        self.assertEqual(len(authors()), 2)
        a = authors(pk=2).first()
        self.assertEqual(a.name, "Mark Seaman")
        self.assertEqual(a.user.username, "mds")
        self.assertEqual(a.bio, "")

    def test_edit_without_login(self):
        response = self.client.get('/writer/author/1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/writer/author/1/')

    def test_edit_get(self):
        self.assertTrue(self.client.login(
            username='johndoe', password='password'))
        response = self.client.get('/writer/author/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Save Record")
        self.assertTemplateUsed(response, 'edit.html')

    def test_author_edit_post(self):
        self.assertTrue(self.client.login(
            username='johndoe', password='password'))
        response = self.client.post('/writer/author/1/', {
            'name': 'John Doe',
            'bio': 'This is my bio',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/writer/author/1')
        self.assertEqual(len(authors()), 1)
        a = authors(pk=1).first()
        self.assertEqual(a.name, "John Doe")
        self.assertEqual(a.user.username, "johndoe")
        self.assertEqual(a.bio, "This is my bio")

    def test_author_delete_view(self):
        response = self.client.get('/writer/author/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure ")
        self.assertTemplateUsed(response, 'delete.html')
