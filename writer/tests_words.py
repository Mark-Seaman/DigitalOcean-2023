from pathlib import Path

from publish.models import Content
from probe.tests_django import DjangoTest
from publish.files import concatonate
from probe.data import save_json_data
from publish.text import text_lines
from writer.words import count_nodes, measure_pub_words

from publish.models import Content, Pub

from probe.tests_django import DjangoTest


class WordCountTest(DjangoTest):

    fixtures = ["config/publish.json"]

    def test_words_in_files(self):
        self.assertEqual('Ok', 'Ok')

    def test_words_in_content_nodes(self):
        text = measure_pub_words()
        # print(len(text_lines(text)), 'Lines of text in word files')
        self.assertEqual(len(text_lines(text)), 1745)

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
