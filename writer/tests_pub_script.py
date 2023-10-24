from pathlib import Path

from publish.files import create_directory
from writer.ai import read_prompt_file

from .pub_script import pub_path, doc_view_data, pub_script
from probe.tests_django import DjangoTest


class PubScriptTest(DjangoTest):

    def test_runs(self):
        self.assertEqual(3, 3)

    def test_create_directory(self):
        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/ghost/AI/test/test/delete-me'
        create_directory(x)
        self.assertTrue(Path(x).exists())

    def test_pub_files(self):
        directory = pub_path('ghost')
        self.assertEqual(str(
            directory), '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/ghost/AI')
        self.assertFiles(directory, 14, 40)

    def test_project(self):
        pub_script(['project', 'ghost'])
        js = (pub_path('ghost').parent)/'pub.json'
        self.assertFileLines(js, 20, 24)

    def test_chapter(self):
        pub_script(['chapter', 'ghost', 'GhostWriter'])
        self.assertFile(pub_path('ghost', 'GhostWriter'))

    def test_doc(self):
        pub_script(['doc', 'ghost', 'GhostWriter', 'B-Ideas.md'])
        self.assertFileLines(
            pub_path('ghost', 'GhostWriter', 'B-Ideas.txt'), 7, 24)
        self.assertFileLines(
            pub_path('ghost', 'GhostWriter', 'B-Ideas.ai'), 12, 24)

    def test_new_doc(self):
        pub_script(['doc', 'ai', 'Creative', 'CreativeWorkflow.md'])
        self.assertFile(pub_path('ai', 'Creative', 'CreativeWorkflow.md'))

    def test_ai_prompt(self):
        path = pub_path('spirituality', 'LifeWithGod', 'Outline.md')
        prompt = read_prompt_file(path)
        # print(prompt)
        self.assertEqual(len(str(prompt)), 398)

    # def test_outline(self):
    #     text = pub_script(
    #         'outline', ['ghost', 'Micropublishing', 'C-Outline.md'])
    #     self.assertNumLines(text, 6, 6)
    #     print(text)

    # def test_chatter(self):
    #     output = 'ghost/AI/Pub/Outline.md'
    #     context = 'ghost/AI/Pub/Persona.md'
    #     content = 'ghost/AI/Pub/TOC.md'
    #     task = 'ghost/AI/Pub/Outline.ai'
    #     task = None   # Disable the AI API call
    #     answer = "Prompt: output=ghost/AI/Pub/Outline.md task=None prompt=None content,context=['ghost/AI/Pub/Persona.md', 'ghost/AI/Pub/TOC.md']"
    #     self.assertEqual(do_gpt_task([output, task, context, content]), answer)

    # def test_chatgpt(self):
    #     x = transform_prompt('write a haiku about trees')
    #     y = ''
    #     # print(x)
    #     self.assertNumLines(x, 3, 3)

    # def test_outline_expander(self):
    #     print(pub_script_command(
    #         'expand', ['ghost', 'Chapter2', 'Chapter2.md']))


def list_files(pub, glob):
    files = [f.name for f in pub_path(pub).glob(glob)]
    return files


def ghost_writer_files(glob):
    return len(list_files('ghost', glob))


def ghost_writer_chapters():
    chapters = doc_view_data(pub='ghost')['chapters']
    return len(chapters)
