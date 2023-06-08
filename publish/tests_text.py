from pathlib import Path
from probe.tests_django import DjangoTest
from .files import read_file, write_file
from .text import word_count


class TextTest(DjangoTest):
    
    def test_word_count(self):
        self.assertEqual(word_count("Hello world"), 2)
        self.assertEqual(word_count("  "), 1)
        self.assertEqual(word_count("  Hello   world  "), 2)
        self.assertEqual(word_count("Hello world"), 2)
        self.assertEqual(word_count("Hello \n\n world \n"), 2)

    def test_read_file(self):
        text = read_file('ReadMe.md')
        self.assertNumLines(text, 173)
        self.assertRange(word_count(text), 1, 496)

    def test_write_file(self):
        f = Path('Test.md')
        write_file(f, read_file('ReadMe.md'))
        text = read_file(f)
        self.assertNumLines(text, 173)
        f.unlink()
    