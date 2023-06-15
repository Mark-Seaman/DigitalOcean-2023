from datetime import datetime

from probe.tests_django import DjangoTest
from os.path import getmtime

from publish.days import is_old

from .models import Content, Pub
from .publication import (all_blogs, all_books, all_privates, all_pubs,
                          build_pubs, get_pub_info, build_pubs)


# -----------------------
# Pub Data Model

class PubDataTest(DjangoTest):

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
        self.assertRange(num, 1200, 1300, "Content objects")

    def test_pub_list(self):
        self.assertRange(len(all_pubs()), 21, 21, 'Num Pubs')

    def test_book_list(self):
        self.assertRange(len(all_books()), 5, 5, 'Num Books')

    def test_blog_list(self):
        self.assertRange(len(all_blogs()), 5, 7, 'Num Blogs')
   
    def test_private_list(self):
        self.assertRange(len(all_privates()), 9, 9, 'Num Private Pubs')

    def test_pub_info(self):
        text = get_pub_info()
        self.assertNumLines(text, 2229, 2319)

    def test_rebuld_pubs(self):
        build_pubs(False, True)
        self.assertRange(len(Pub.objects.all()), 21, 21)
        self.assertRange(len(Content.objects.all()), 1200, 1300, "Content Nodes")
        self.assertNumLines(get_pub_info(), 2229, 2319)

    def test_data_file(self):
        self.assertFalse(is_old("config/publish.json"), 'config/publish.json is old')

