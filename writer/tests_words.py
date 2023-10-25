from probe.tests_django import DjangoTest
from publish.text import text_lines
from writer.words import count_nodes, measure_pub_words

from probe.tests_django import DjangoTest


class WordCountTest(DjangoTest):

    fixtures = ["config/publish.json"]

    def test_words_in_content_nodes(self):
        text = measure_pub_words()
        self.assertNumLines(text, 1726, 1750, 'Lines in word count files')

    def test_content_nodes(self):
        pubs, contents, words, pages = count_nodes()
        self.assertRange(pubs, 19, 19)
        self.assertRange(contents, 1320, 1330)
        self.assertRange(pages, 1800, 1900)
        self.assertRange(words, 471000, 474000)
