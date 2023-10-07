from csv import reader
from pathlib import Path

from django.forms import model_to_dict

from probe.tests_django import DjangoTest
from publish.days import is_old
from publish.publication import count_pub_words, get_pub, list_publications, show_pub_details


class PubDocTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_all_docs(self):
        self.assertFiles('Documents', 500, 2600)

    def test_doc_directories(self):
        data = '''Documents/SHRINKING-WORLD-PUBS,1048,1060'''
        for x in list(reader(data.splitlines())):
            # print(x)
            if x[2:]:
                self.assertFiles(x[0], int(x[1]), int(x[2]))
            else:
                self.assertFiles(x[0], int(x[1]), int(x[1]))

    def test_pub_list(self):
        self.assertRange(len(list_publications()), 4, 20)

    def test_model_to_dict(self):
        p = get_pub('journey')
        x = model_to_dict(p, fields=['id', 'name', 'doc_path'], exclude=['id'])
        y = {'name': 'journey',
             'doc_path': 'Documents/Shrinking-World-Pubs/journey/Pub'}
        self.assertEqual(x, y)

    def test_pub_words(self):
        words = [
            ('sweng', 21509),
            ('leverage', 83659),
            ('webapps', 49888),
            ('journey', 66160),
            ('quest', 56823),
            ('poem', 16876),
        ]
        for p in words:
            pub_name = p[0]
            x = count_pub_words(pub_name)
            self.assertEqual(x, p[1])
