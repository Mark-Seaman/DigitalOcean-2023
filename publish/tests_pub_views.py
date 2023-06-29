from django.test import TestCase

from probe.tests_django import DjangoTest
from .publication import pub_redirect

from .models import Content, Pub

# -----------------------
# Local Blog Pub Pages

local_host = 'http://localhost:8000'


class BlogPageTest(DjangoTest):
    def test_pub_redirect(self):
        redirects = (("shrinking-world.com", None, None, '/pubs/book'),
                     ("seamansguide.com", "journey","Index.md", '/journey/Index.md'),
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
            self.assertEqual(pub_redirect(r[0], r[1], r[2]), r[3], f'FAILED: {r}')
