from probe.tests_django import DjangoTest
from publish.text import text_lines

from .outline import (create_index, extract_links,
                      extract_outlines, extract_urls, create_outlines)
from .playmaker import read_outline, read_plays, write_playbook, write_plays
from .pub_script import pub_path


class PlaymakerTest(DjangoTest):

    def test_outline(self):
        x = read_outline('apps')
        self.assertEqual(len(text_lines(x)), 59)

    def test_plays(self):
        x = read_plays('apps')
        self.assertEqual(len(x), 47)

    def test_write_plays(self):
        x = write_plays('apps')
        self.assertEqual(len(x), 47)

    def test_write_playbook(self):
        x = write_playbook('apps')
        self.assertEqual(len(x), 2)
