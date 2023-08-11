from probe.tests_django import DjangoTest
from publish.files import read_csv_file
from publish.text import text_lines
from writer.pub_script import pub_path

from .playmaker import (publish_playbook, title_map, read_outline, read_plays, read_toc, write_chapters, write_contents, write_index,
                        write_playbook, write_plays_csv)


class PlaymakerTest(DjangoTest):

    def test_outline(self):
        x = read_outline('apps')
        # print(x)
        # print('---')
        self.assertEqual(len(x), 57)
        self.assertEqual(x[0], 'AI Playbook for web app development')
        self.assertEqual(x[1], '    Using This Playbook')
        self.assertEqual(x[2], '        Problem - Prompts - Prompt Engineering')
        self.assertEqual(x[50], '    Devops')

    def test_plays(self):
        plays = read_plays('apps')
        self.assertEqual(len(plays), 56)
        self.assertEqual(plays[0][0],'Playbook.md')  
        self.assertEqual(plays[0][1],'AI Playbook for web app development')  
        # for y in x:
        #     print(y)

    def test_chapter_files(self):
        plays = read_plays('apps')
        titles = {row[2].strip(): row[0] for row in plays}
        lines =  read_outline('apps')
        text = ''
        for i,line in enumerate(lines):
            default = line.replace(' ', '')+'.md'
            file = titles.get(line.strip(), default)
            if not line.startswith('        '):
                c = i
            row = f'{file},{c},{i},{line}'
            text += row+'\n'
        write_plays_csv('apps', text)
        
        # print(x.keys())
        # self.assertEqual(list(x.keys())[4], 'Develop Your Own Strategy')
        # self.assertEqual(x['Develop Your Own Strategy'], '')


    def test_write_plays(self):
        x = write_plays_csv('apps')
        self.assertEqual(x, '57 Lines in playlist')


    # # xoox
    # def test_write_index(self):
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
