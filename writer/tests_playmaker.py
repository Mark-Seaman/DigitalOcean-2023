from probe.tests_django import DjangoTest
from publish.text import text_lines

from .playmaker import (read_outline, read_plays, write_chapters, write_contents, write_index,
                        write_playbook, write_plays_csv)


class PlaymakerTest(DjangoTest):

    def test_outline(self):
        x = read_outline('apps')
        self.assertEqual(len(text_lines(x)), 59)

    def test_plays(self):
        x = read_plays('apps')
        self.assertEqual(len(x), 57)

    def test_write_plays(self):
        x = write_plays_csv('apps')
        self.assertEqual(x, '58 Lines in playlist')

    # def test_write_index(self):
    #     x = write_index()
    #     self.assertEqual(x, 'Not Implemented')

    def test_write_contents(self):
        x = write_contents('apps')
        self.assertEqual(x, '58 Lines in contents file')

    def test_chapters(self):
        x = write_chapters('apps')
        self.assertEqual(x, '10 Chapters')

   # def test_write_playbook(self):
    #     x = write_playbook('apps')
    #     self.assertEqual(len(x), 2)
