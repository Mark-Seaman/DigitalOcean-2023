from probe.tests_django import DjangoTest
from publish.publication import pub_redirect


class RemoteBlogPagesTest(DjangoTest):
    def test_blog_seamanslog(self):
        self.assertPageLines("https://seamanslog.com", 100, 310)

    def test_blog_spirit(self):
        self.assertPageLines("https://spiritual-things.org", 100, 310)

    def test_blog_mark_seaman(self):
        self.assertPageLines("https://markseaman.org", 120, 310)


class BlogFilesTest(DjangoTest):
    def test_seamanslog(self):
        self.assertFiles("Documents/seamanslog.com", 380, 400)

    def test_spiritlog(self):
        self.assertFiles("Documents/spiritual-things.org/daily", 370, 380)


local_host = 'http://localhost:8000'


class BlogPageTest(DjangoTest):
    def test_pub_redirect(self):
        redirects = (("shrinking-world.com", None, None, '/pubs/book'),
                     ("seamansguide.com", "journey",
                      "Index.md", '/journey/Index.md'),
                     ("seamansguide.com", None, "journey", '/pubs/book'),
                     ("seamansguide.com", "journey", None, '/journey'),
                     ("seamansguide.com", None, None, '/pubs/book'),
                     ("seamanslog.com", None, None, '/sampler'),
                     ("seamanfamily.org", None, None, '/family/Index.md'),
                     ("spiritual-things.org", None, None, '/spiritual'),
                     ("markseaman.org", None, None, '/marks/contact'),
                     ("markseaman.info", None, None, '/private'),
                     ("localhost:8000", None, None, '/pubs/book'))
        for r in redirects:
            self.assertEqual(pub_redirect(
                r[0], r[1], r[2]), r[3], f'FAILED: {r}')
