from probe.tests_django import DjangoTest
from writer.outline import (create_index, extract_links, extract_outlines,
                            extract_urls, create_outlines)

from .pub_script import pub_path


class OutlineTest(DjangoTest):

    def test_outline_urls(self):
        path = pub_path('spirituality','Transformation','Index.md')
        x = extract_urls(path)
        self.assertEqual(len(x), 6)

    def test_outline_links(self):
        path = pub_path('spirituality','Transformation','Index.md')
        x = extract_links(path)
        self.assertEqual(len(x), 6)

    def test_create_index(self):
        path = pub_path('spirituality','Worship')
        create_index(path)
        
    def test_outlines(self):
        path = pub_path('spirituality','Worship')
        create_outlines(path)
        
        # x = '\n'.join([x for x in x])
        # self.assertEqual(len(x), 1047)

    

