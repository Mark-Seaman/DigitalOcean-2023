from csv import reader
from django.forms import model_to_dict

from probe.tests_django import DjangoTest
from publish.publication import get_pub, list_publications, work_pending

pub_words = [
    ('leverage', 83659, 83659),
    ('journey',  66160, 67732),
    ('quest',    56823, 57499),
    ('webapps',  49888, 49888),
    ('sweng',    7526, 28592),
    ('poem',     16876, 16876),
]

unpub_words = [
    ('spiritual',   60709),
    ('sampler',     58288),
    ('tech',        22541),
    ('write',       8231),
    ('spirituality', 9803),
    ('ai',          9449),
    ('today',       717),
    # ('bacs350', 0),
    # ('cs350', 0),
]


class PubDocTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_all_docs(self):
        self.assertFiles('Documents', 2500, 2700)

    def test_doc_directories(self):
        data = '''
            Documents/SHRINKING-WORLD-PUBS,1080,1300
            Documents/SHRINKING-WORLD-PUBS/journey,65,85
            Documents/SHRINKING-WORLD-PUBS/quest,73,73
            Documents/SHRINKING-WORLD-PUBS/poem,92,92
            Documents/SHRINKING-WORLD-PUBS/leverage,24,24
            Documents/SHRINKING-WORLD-PUBS/sweng,142,160
            Documents/SHRINKING-WORLD-PUBS/webapps,88,88
            '''
        for x in list(reader(data.splitlines())):
            if x and x[0].strip():
                if x[2:]:
                    self.assertFiles(x[0].strip(), int(x[1]), int(x[2]))
                else:
                    self.assertFiles(x[0].strip(), int(x[1]), int(x[1]))

    def test_pub_list(self):
        self.assertRange(len(list_publications()), 4, 20)

    def test_model_to_dict(self):
        p = get_pub('journey')
        x = model_to_dict(p, fields=['id', 'name', 'doc_path'], exclude=['id'])
        y = {'name': 'journey',
             'doc_path': 'Documents/Shrinking-World-Pubs/journey/Pub'}
        self.assertEqual(x, y)

    def test_pub_words(self):
        for p in pub_words:
            pub = get_pub(p[0])
            self.assertRange(pub.words, p[1], p[2], f'Words in {pub.name}')

    # def test_unpub_words(self):
    #     for p in unpub_words:
    #         pub_name = p[0]
    #         x = count_pub_words(pub_name)
    #         self.assertEqual(x, p[1])

    # def test_ai_docs(self):
    #     work_pending()
