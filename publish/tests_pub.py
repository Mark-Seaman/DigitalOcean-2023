from os import system
from pathlib import Path
from django.test import SimpleTestCase, TestCase
from requests import get

from .models import Pub, Content
from .pub import all_blogs, all_books, build_pubs
from .text import text_lines


class DjangoTest(TestCase):
    def assertFiles(self, directory, min, max):
        num_files = len([f for f in Path(directory).rglob("*.md")])
        error = f"files in {directory}: {num_files} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num_files, min, error)
        self.assertLessEqual(num_files, max, error)

    def assertLines(self, page, min, max):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        lines = len(text_lines(response.text))
        self.assertRange(lines, min, max, label=f"Lines in {page}")

    def assertText(self, page, text):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        self.assertIn(text, response.text)

    def assertRange(self, num, min, max, label="Value"):
        error = f"{label} {num} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num, min, error)
        self.assertLessEqual(num, max, error)


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


# -----------------------
# Local Blog Pub Pages


class BlogPageTest(DjangoTest):
    def test_home_page(self):
        page = "http://localhost:8000/"
        self.assertLines(page, 180, 190)

    def test_sampler_page(self):
        page = "http://localhost:8000/sampler"
        self.assertText(page, "Seaman&#x27;s Log")

    def test_index_page(self):
        page = "http://localhost:8000/sampler/Index"
        self.assertText(page, "Seaman&#x27;s Log")
        page = "http://localhost:8000/sampler/Index.md"
        self.assertText(page, "Seaman&#x27;s Log")

    def test_spirit_page(self):
        page = "http://localhost:8000/spiritual"
        self.assertText(page, "Meditations")

    def test_tech_page(self):
        page = "http://localhost:8000/tech"
        self.assertText(page, "Tech Notes")

    def test_write_page(self):
        page = "http://localhost:8000/write"
        self.assertText(page, "Writer's Block")

    def test_tech_page(self):
        page = "http://localhost:8000/mark"
        self.assertText(page, "Mark David Seaman")


# -----------------------
# Local Book Pub Pages


class BookPageTest(DjangoTest):
    def test_book_list_page(self):
        page = "http://localhost:8000/publish/book"
        self.assertLines(page, 200, 244)

    def test_book_journey_page(self):
        page = "http://localhost:8000/journey"
        self.assertLines(page, 190, 200)


# -----------------------
# Local Book Pub Pages

# def test_tweet_view(self):
#     self.assertTrue(Path("Documents/shrinking-world.com/tweet/20917.md").exists())

# def test_tweet_view(self):
#     response = self.client.get("/0")
#     self.assertEqual(response.status_code, 200)
#     self.assertTemplateUsed(response, "theme.html")
#     self.assertTemplateUsed(response, "tweet.html")
