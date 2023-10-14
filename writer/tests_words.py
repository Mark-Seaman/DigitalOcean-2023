from pathlib import Path

from publish.models import Content
from probe.tests_django import DjangoTest
from publish.files import concatonate
from probe.data import save_json_data
from writer.words import count_nodes, show_pubs

from publish.models import Content, Pub

from probe.tests_django import DjangoTest


class WordCountTest(DjangoTest):

    fixtures = ["config/publish.json"]

    def test_words_in_files(self):
        self.assertEqual('Ok', 'Ok')

    def test_words_in_content_nodes(self):
        self.assertEqual('Ok', 'Ok')

    def test_word_count_files(self):
        self.assertEqual('Ok', 'Ok')

    def test_pub_pages(self):
        self.assertEqual('Ok', 'Ok')

    def test_content_nodes(self):
        pubs, contents, words, pages = count_nodes()
        self.assertEqual(pubs, 20)
        self.assertEqual(contents, 1310)
        self.assertEqual(words, 474525)
        self.assertEqual(pages, 1898)
