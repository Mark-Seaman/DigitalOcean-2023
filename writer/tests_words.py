from probe.tests_django import DjangoTest
from publish.text import text_lines
from writer.words import count_nodes, measure_pub_words

from probe.tests_django import DjangoTest


class WordCountTest(DjangoTest):

    fixtures = ["config/publish.json"]

    def test_words_in_files(self):
        self.assertEqual('Ok', 'Ok')

    def test_words_in_content_nodes(self):
        text = measure_pub_words()
        # print(len(text_lines(text)), 'Lines of text in word files')
        self.assertEqual(len(text_lines(text)), 1726)

    def test_content_nodes(self):
        pubs, contents, words, pages = count_nodes()
        self.assertEqual(pubs, 19)
        self.assertEqual(contents, 1314)
        self.assertEqual(words, 470281)
        self.assertEqual(pages, 1881)
