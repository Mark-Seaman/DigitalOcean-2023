from probe.tests_django import DjangoTest
from .pub_script import pub_script


class CoverImageTest(DjangoTest):
    def test_web_page(self):
        pub_script(['cover', 'write'])
        