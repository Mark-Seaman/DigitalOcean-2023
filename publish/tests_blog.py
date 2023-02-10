from pathlib import Path

from .tests_pub import DjangoTest


class RemoteBlogPagesTest(DjangoTest):
    def test_blog_seamanslog(self):
        self.assertLines("https://seamanslog.com", 100, 130)

    def test_blog_spirit(self):
        self.assertLines("https://spiritual-things.org", 100, 121)

    def test_blog_tech_notes(self):
        self.assertLines(
            "https://shrinking-world.com/tech/tech-Index", 100, 120)

    def test_blog_micropub(self):
        self.assertLines(
            "https://shrinking-world.com/tech/micropub-Index", 100, 140)

    def test_blog_training(self):
        self.assertLines(
            "https://shrinking-world.com/tech/training-Index", 100, 120)

    def test_blog_mark_seaman(self):
        self.assertLines("https://markseaman.org", 150, 170)


class BlogFilesTest(DjangoTest):
    def test_seamanslog(self):
        self.assertFiles("Documents/seamanslog.com", 390, 410)

    def test_spiritlog(self):
        self.assertFiles("Documents/spiritual-things.org/daily", 370, 380)

    def test_tech_notes(self):
        self.assertFiles("Documents/shrinking-world.com/blog", 28, 50)
