from csv import reader

from probe.tests_django import DjangoTest
from publish.publication import all_pubs, get_pub_info, list_publications


class PubDocTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_all_docs(self):
        self.assertFiles('Documents', 2051, 2070)

    def test_doc_directories(self):
        data = '''Documents,2051,2070
Documents/seamansguide.com,200,322
Documents/seamanslog.com,405
Documents/markseaman.org,19
Documents/markseaman.info,65
Documents/shrinking-world.com,548
Documents/shrinking-world.io,59
Documents/shrinking-world.org,3
Documents/spiritual-things.org,431
Documents/SHRINKING-WORLD-PUBS,183,400
'''
        for x in list(reader(data.splitlines())):
            # print(x)
            if x[2:]:
                self.assertFiles(x[0], int(x[1]), int(x[2]))
            else:
                self.assertFiles(x[0], int(x[1]), int(x[1]))

    def test_pub_list(self):
        self.assertRange(len(list_publications()), 21, 21)