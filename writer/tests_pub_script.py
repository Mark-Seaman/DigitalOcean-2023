from pathlib import Path

from publish.files import create_directory

from .pub_script import (doc_html, doc_list, doc_text, doc_title, pub_list,
                      pub_path, doc_view_data, pub_script, read_pub_doc)
from probe.tests_django import DjangoTest


class PubScriptTest(DjangoTest):

    def test_runs(self):
        self.assertEqual(3, 3)

    def test_create_directory(self):
        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/test/test/delete-me'
        create_directory(x)
        self.assertTrue(Path(x).exists())

    def test_pub_files(self):
        directory = pub_path('GhostWriter')
        self.assertEqual(str(
            directory), '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        self.assertFiles(directory, 14, 40)

    def test_project(self):
        pub_script(['project', 'GhostWriter'])
        js = (pub_path('GhostWriter').parent)/'pub.json'
        self.assertFileLines(js, 20, 24)

    def test_chapter(self):
        pub_script(['chapter', 'GhostWriter', 'GhostWriter'])
        self.assertFile(pub_path('GhostWriter', 'GhostWriter'))

    def test_doc(self):
        pub_script(['doc', 'GhostWriter', 'GhostWriter', 'B-Ideas.md'])
        self.assertFileLines(
            pub_path('GhostWriter', 'GhostWriter', 'B-Ideas.txt'), 7, 24)
        self.assertFileLines(
            pub_path('GhostWriter', 'GhostWriter', 'B-Ideas.ai'), 12, 24)
    
    def test_new_doc(self):
        pub_script(['doc', 'ai', 'Creative', 'CreativeWorkflow.md'])
        self.assertFile(pub_path('ai', 'Creative', 'CreativeWorkflow.md'))

    # def test_outline(self):
    #     text = pub_script_command(
    #         'outline', ['GhostWriter', 'Micropublishing', 'C-Outline.md'])
    #     self.assertNumLines(text, 6, 6)
    #     # print(text)

    # def test_chatter(self):
    #     output = 'GhostWriter/AI/Pub/Outline.md'
    #     context = 'GhostWriter/AI/Pub/Persona.md'
    #     content = 'GhostWriter/AI/Pub/TOC.md'
    #     task = 'GhostWriter/AI/Pub/Outline.ai'
    #     task = None   # Disable the AI API call
    #     answer = "Prompt: output=GhostWriter/AI/Pub/Outline.md task=None prompt=None content,context=['GhostWriter/AI/Pub/Persona.md', 'GhostWriter/AI/Pub/TOC.md']"
    #     self.assertEqual(do_gpt_task([output, task, context, content]), answer)

    # def test_chatgpt(self):
    #     x = transform_prompt('write a haiku about trees')
    #     y = ''
    #     # print(x)
    #     self.assertNumLines(x, 3, 3)

    # def test_outline_expander(self):
    #     print(pub_script_command(
    #         'expand', ['GhostWriter', 'Chapter2', 'Chapter2.md']))


def list_files(pub, glob):
    files = [f.name for f in pub_path(pub).glob(glob)]
    return files


def ghost_writer_files(glob):
    return len(list_files('GhostWriter', glob))


def ghost_writer_chapters():
    chapters = doc_view_data(pub='GhostWriter')['chapters']
    return len(chapters)

