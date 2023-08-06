from probe.tests_django import DjangoTest
from publish.text import text_lines

from .playmaker import (publish_playbook, read_outline, read_plays, read_toc, write_chapters, write_contents, write_index,
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

    def test_write_index(self):
        x = write_index('apps')
        # xxoooooooooo
        self.assertEqual(x, '101 Lines in Index')

    def test_write_contents(self):
        x = write_contents('apps')
        self.assertEqual(x, '58 Lines in contents file')

    def test_chapters(self):
        x = write_chapters('apps')
        self.assertEqual(x, '10 Chapters')

    def test_toc(self):
        cmap, fmap = read_toc('apps')
        self.assertEqual(len(cmap), 10)
        self.assertEqual(len(fmap), 58)

    # xooxxooxx0
    def test_publish_playbook(self):
        x = publish_playbook('apps')
        self.assertEqual(x, 'OK')


   # def test_write_playbook(self):
    #     x = write_playbook('apps')
    #     self.assertEqual(len(x), 2)
