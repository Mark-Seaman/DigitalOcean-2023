from pathlib import Path

from publish.files import create_directory
from writer.tests_pub_script import ghost_writer_files

from .pub_script import (doc_html, doc_list, doc_text, pub_doc_title, pub_list,
                         pub_path, doc_view_data, pub_script, read_pub_doc)
from probe.tests_django import DjangoTest


class PubTest(DjangoTest):

    def test_pub_path(self):
        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs')
        self.assertEqual(pub_path(), x)

        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/ghost/AI')
        self.assertEqual(pub_path('ghost'), x)

        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/ghost/AI/Chapter1'
        self.assertEqual(str(pub_path('ghost', 'Chapter1')), x)

        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/ghost/AI/Chapter1/Chapter1.md'
        self.assertEqual(
            str(pub_path('ghost', 'Chapter1', 'Chapter1.md')), x)

    def test_num_pubs(self):
        pubs1 = len(pub_list())
        pubs2 = len(doc_view_data()['pubs'])
        self.assertEqual(pubs1, pubs2)
        self.assertRange(pubs2, 7, 17)

    def test_doc_files(self):
        self.assertRange(ghost_writer_files('*/*.md'), 28, 40)

    def test_ai_files(self):
        self.assertRange(ghost_writer_files('*/*.ai'), 20, 39)

    def test_txt_files(self):
        self.assertRange(ghost_writer_files('*/*.txt'), 15, 18)

    def test_chapters(self):
        chapters = doc_view_data(pub='ghost')['chapters']
        self.assertRange(len(chapters), 7, 11)

    def test_doc_list(self):
        y = doc_list('ghost', 'WritersGuide')
        self.assertEqual(len(y), 6)

    def test_load_doc(self):
        x = '# Chapter 1 - Introduction'
        y = read_pub_doc('ghost', 'WritersGuide', 'Chapter1.md')[:26]
        self.assertEqual(y, x)

        x = doc_view_data(pub='ghost', chapter='WritersGuide',
                          doc='Chapter1.md')['text'][:26]
        self.assertEqual(y, x)

    def test_doc_title(self):
        x = 'Chapter 1 - Introduction'
        y = pub_doc_title('ghost', 'WritersGuide', 'Chapter1.md')
        self.assertEqual(y, x)

    def test_doc_text(self):
        x = '    1.1. Purpose of '
        y = doc_text('ghost', 'WritersGuide', 'Chapter1.md')[:20]
        self.assertEqual(y, x)

    def test_doc_html(self):
        html = doc_html('ghost', 'WritersGuide', 'Chapter1.md')
        self.assertNumLines(html, 128, 130)
        html = doc_view_data(
            pub='ghost', chapter='WritersGuide', doc='Chapter1.md')['html']
        self.assertNumLines(html, 128, 130)
