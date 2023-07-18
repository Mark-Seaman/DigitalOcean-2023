
from writer.outline import extract_links, extract_outlines, extract_urls, test_extraction

from .pub_script import pub_path 
from probe.tests_django import DjangoTest


class OutlineTest(DjangoTest):

    def test_outline_urls(self):
        path = pub_path('spirituality','Transformation','Index.md')
        x = extract_urls(path)
        self.assertEqual(len(x), 6)

    def test_outline_links(self):
        path = pub_path('spirituality','Transformation','Index.md')
        x = extract_links(path)
        self.assertEqual(len(x), 6)

    # def test_outlines(self):
    #     path = pub_path('spirituality','Transformation','Outline.md')
    #     x = extract_outlines(path)
    #     x = '\n'.join([x for x in x])
    #     self.assertEqual(len(x), 1047)
