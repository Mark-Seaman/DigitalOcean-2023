
from django.test import TestCase

from .models import Content, Pub
from .pub import all_blogs, all_books, build_pubs
from probe.tests_django import DjangoTest


# -----------------------
# Pub Data Model

class PubDataTest(TestCase):

    # Pub Data Model
    def setup(self):
        blog1 = Pub.objects.create()

    def test_blog_add(self):
        blog1 = Pub.objects.create(
            name="Write", title="Authoring Tips", url="write")
        blog2 = Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        self.assertEqual(len(Pub.objects.all()), 2)

    def test_blog_detail(self):

        Pub.objects.create(name="Write", title="Authoring Tips", url="write")
        Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        blog1 = Pub.objects.get(name="Write")
        blog2 = Pub.objects.get(title="Pro Pub", url="tech")
        self.assertEqual(blog1.title, "Authoring Tips")
        self.assertEqual(blog1.url, "write")
        self.assertEqual(blog2.url, "tech")

    def test_blog_edit(self):

        Pub.objects.create(name="Write", title="Authoring Tips", url="write")
        Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        blog1 = Pub.objects.get(name="Write")
        blog2 = Pub.objects.get(title="Pro Pub", url="tech")
        blog1.title = "New Tips"
        blog1.url = "newurl"
        self.assertEqual(blog1.title, "New Tips")
        self.assertEqual(blog1.url, "newurl")
        self.assertEqual(blog2.url, "tech")



# -----------------------
# Build Pubs


class PubInputOutputTest(DjangoTest):
    def test_build_blogs(self):
        build_pubs()
        self.assertEqual(len(Pub.objects.all()), 21)
        num = len(Content.objects.all())
        self.assertRange(num, 1200, 1300, "Blog Contents")


# -----------------------
# Pub Fixture


class FixtureTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_with_data(self):
        num = len(Content.objects.all())
        self.assertRange(num, 1200, 1300, "Blog Contents")

    def test_book_list(self):
        self.assertRange(len(all_books()), 5, 5)

    def test_blog_list(self):
        self.assertRange(len(all_blogs()), 5, 7)
