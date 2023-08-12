from probe.tests_django import DjangoTest
from publish.files import read_csv_file, write_file
from publish.text import text_lines
from writer.pub_script import pub_path

from .playmaker import (chapter_index, create_docs, publish_playbook, title_map, read_outline, read_plays, read_toc, write_chapters, write_contents, write_index,
                        write_playbook, write_plays_csv)


class PlaymakerTest(DjangoTest):

    def test_outline(self):
        x = read_outline('apps')
        self.assertEqual(len(x), 56)
        self.assertEqual(x[0], 'AI Playbook for web app development')
        self.assertEqual(x[1], '    Using This Playbook')
        self.assertEqual(
            x[2], '        Problem - Prompts - Prompt Engineering')
        self.assertEqual(x[50], '    Devops')

    def test_plays(self):
        plays = read_plays('apps')
        self.assertEqual(len(plays), 56)
        self.assertEqual(plays[0][0], 'Playbook.md')
        self.assertEqual(plays[0][3], 'AI Playbook for web app development')

    def test_title_map(self):
        plays = read_plays('apps')
        titles = {row[3].strip(): row[0] for row in plays}
        x = titles.get('Problem - Prompts - Prompt Engineering')
        self.assertEqual(x, 'PromptEngineering.md')

    def test_write_plays(self):
        x = write_plays_csv('apps')
        self.assertEqual(x, '57 Lines in playlist')

    def test_create_docs(self):
        create_docs('apps')
        self.assertTrue(pub_path('apps', 'Views', 'Views.md').exists())

    def test_chapter_index(self):
        chapter_index('apps', '4', '15')
        p = pub_path('apps', 'Hosting', 'Index.md')
        # print(text_lines(p.read_text())[4])
        x = text_lines(p.read_text())[4]
        self.assertTrue(x, '* [App Platform - Static Server](StaticServer)')

    def test_write_index(self):
        x = read_plays('apps')
        plays = [y for y in x if y[1] == y[2]]
        for i, p in enumerate(plays):
            chapter_index('apps', i, str(p[1]))

    #     x = write_index('apps')
    #     self.assertEqual(x, '101 Lines in Index')

    # def test_write_contents(self):
    #     x = write_contents('apps')
    #     self.assertEqual(x, '58 Lines in contents file')

    # def test_chapters(self):
    #     x = write_chapters('apps')
    #     self.assertEqual(x, '10 Chapters')

    def test_toc(self):
        cmap, fmap = read_toc('apps')
        self.assertEqual(len(cmap), 8)
        self.assertEqual(len(fmap), 57)

    # xooxxooxxoxo
    def test_publish_playbook(self):
        x = publish_playbook('apps')
        self.assertEqual(x, 'OK')

   # def test_write_playbook(self):
    #     x = write_playbook('apps')
    #     self.assertEqual(len(x), 2)
