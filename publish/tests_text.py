from pathlib import Path

from probe.tests_django import DjangoTest
from publish.shell import shell

from .files import concatonate, read_file, recursive_files, write_file
from .text import line_count, text_join, text_lines, word_count


class TextFileTest(DjangoTest):

    def test_word_count(self):
        self.assertEqual(word_count("Hello world"), 2)
        self.assertEqual(word_count("  "), 1)
        self.assertEqual(word_count("  Hello   world  "), 2)
        self.assertEqual(word_count("Hello world"), 2)
        self.assertEqual(word_count("Hello \n\n world \n"), 2)

    def test_read_file(self):
        text = read_file('ReadMe.md')
        self.assertNumLines(text, 160)
        self.assertRange(word_count(text), 1, 600)

    def test_write_file(self):
        f = Path('Test.md')
        write_file(f, read_file('ReadMe.md'))
        text = read_file(f)
        self.assertNumLines(text, 160)
        f.unlink()

    def test_file_list(self):
        files = len(list(Path('probe').glob('**/*')))
        self.assertRange(files, 84, 120, f'files in probe file tree')

    def test_concatonate(self):
        text = concatonate('probe/**/*.py')
        self.assertNumLines(
            text, 1150, 1250, f'lines in Python files for probe file tree')

    def test_recursive_files(self):
        files = recursive_files('probe')
        self.assertRange(len(files), 84, 120, f'files in probe file tree')

    def test_line_count(self):
        self.assertEqual(line_count('x'), 1)
        self.assertEqual(line_count('  '), 1)
        self.assertEqual(line_count('  \n'), 2)
        self.assertEqual(line_count('  \n \n '), 3)
        self.assertEqual(line_count('a\nb\nc\nd'), 4)
        self.assertEqual(line_count('\n'), 2)
        self.assertEqual(line_count('\n\n\n'), 4)

    def test_shell(self):
        self.assertEqual(shell('echo hello'), 'hello\n')
        text = text_lines(shell('ls'))
        self.assertEqual(len(text), 15)

    def test_text_lines(self):
        self.assertEqual(text_lines('x'), ['x'])
        self.assertEqual(text_lines('x\n'), ['x', ''])
        self.assertEqual(text_lines('x\ny'), ['x', 'y'])
        self.assertEqual(text_lines('x\ny\nz'), ['x', 'y', 'z'])

    def test_text_join(self):
        self.assertEqual(text_join(text_lines('x\ny\nz')), 'x\ny\nz')
