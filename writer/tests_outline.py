from probe.tests_django import DjangoTest
from publish.files import concatonate
from writer.outline import (create_index, create_slides_text, extract_links,
                            extract_urls, create_outlines, headings_format, read_outline, slides_format, split_outline)

from .pub_script import pub_path


class OutlineTest(DjangoTest):

    def test_outline_urls(self):
        path = pub_path('spirituality', 'Transformation', 'Index.md')
        x = extract_urls(path)
        self.assertEqual(len(x), 6)

    def test_outline_links(self):
        path = pub_path('spirituality', 'Transformation', 'Index.md')
        x = extract_links(path)
        self.assertEqual(len(x), 5)

    def test_create_index(self):
        path = pub_path('spirituality', 'Worship')
        create_index(path)

    def test_ai_prompts(self):
        path = pub_path('spirituality', 'Worship')
        create_outlines(path)
        # path = pub_path('spirituality', 'Worship')
        path = 'Documents/Shrinking-World-Pubs/spirituality/AI/Worship/*.ai'
        text = concatonate(path)
        self.assertNumLines(text, 53, 53, f'lines AI Prompt')

    def test_split_outline(self):
        path = pub_path('spirituality', 'Worship', 'Outline.md')
        text = create_slides_text(path)
        # print(text)
        self.assertNumLines(text, 23, 23, f'lines in Slides')

    def test_slides(self):
        path = pub_path('writer', 'CreativeLifecycle', 'Outline.md')
        text = read_outline(path)
        text = slides_format(text)
        # print(text)
        self.assertNumLines(text, 27, 27, f'lines in Slides')

    def test_headings(self):
        path = pub_path('writer', 'CreativeLifecycle', 'Outline.md')
        text = read_outline(path)
        text = headings_format(text)
        # print(text)
        o = split_outline(text)[1:]
        for i in o:
            #     # print(i['title'])
            print('##', slides_format(i['outline']))
            print('\n---\n')
