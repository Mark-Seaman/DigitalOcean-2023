from .tests_pub_views import DjangoTest


class RemoteBlogPagesTest(DjangoTest):
    def test_blog_seamanslog(self):
        self.assertPageLines("https://seamanslog.com", 180, 190)

    def test_blog_spirit(self):
        self.assertPageLines("https://spiritual-things.org", 100, 121)

    def test_blog_tech_notes(self):
        self.assertPageLines(
            "https://shrinking-world.com/tech/tech-Index", 100, 120)

    def test_blog_micropub(self):
        self.assertPageLines(
            "https://shrinking-world.com/tech/micropub-Index", 100, 140)

    def test_blog_training(self):
        self.assertPageLines(
            "https://shrinking-world.com/tech/training-Index", 100, 120)

    def test_blog_mark_seaman(self):
        self.assertPageLines("https://markseaman.org", 150, 170)


class BlogFilesTest(DjangoTest):
    def test_seamanslog(self):
        self.assertFiles("Documents/seamanslog.com", 380, 400)

    def test_spiritlog(self):
        self.assertFiles("Documents/spiritual-things.org/daily", 370, 380)

 