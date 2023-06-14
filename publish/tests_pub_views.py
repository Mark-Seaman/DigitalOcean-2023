from django.test import TestCase

from probe.tests_django import DjangoTest

from .models import Content, Pub

# -----------------------
# Local Blog Pub Pages


class BlogPageTest(DjangoTest):
    def test_home_page(self):
        page = "http://localhost:8000/"
        self.assertPageLines(page, 180, 190)

    def test_bouncer_page(self):
        page = "/11"
        url = "https://shrinking-world.com/tech/shrinkingworld-ContactMe.md"
        self.assertPageRedirect(page, url)
        page = "/81"
        url = "https://seamansguide.com/journey"
        self.assertPageRedirect(page, url)
        page = "http://localhost:8000/sampler"
        self.assertPageText(page, "Seaman&#x27;s Log")

    def test_sampler_page(self):
        page = "http://localhost:8000/sampler"
        self.assertPageText(page, "Seaman&#x27;s Log")

    def test_index_page(self):
        page = "http://localhost:8000/sampler/Index"
        self.assertPageText(page, "Seaman&#x27;s Log")
        page = "http://localhost:8000/sampler/Index.md"
        self.assertPageText(page, "Seaman&#x27;s Log")

    def test_spirit_page(self):
        page = "http://localhost:8000/spiritual"
        self.assertPageText(page, "Meditations")

    def test_tech_page(self):
        page = "http://localhost:8000/tech"
        self.assertPageText(page, "Tech Notes")

    def test_write_page(self):
        page = "http://localhost:8000/write"
        self.assertPageText(page, "Writer's Block")

    def test_tech_page(self):
        page = "http://localhost:8000/mark"
        self.assertPageText(page, "Mark David Seaman")


# -----------------------
# Local Book Pub Pages

class BookPageTest(DjangoTest):
    def test_book_list_page(self):
        page = "http://localhost:8000/publish/book"
        self.assertPageLines(page, 200, 244)

    def test_book_journey_page(self):
        page = "http://localhost:8000/journey"
        self.assertPageLines(page, 190, 200)
