from csv import reader
from probe.tests_django import DjangoTest


class PubDocTest(DjangoTest):
    def test_all_docs(self):
        self.assertFiles('Documents', 2051, 2051)

    def test_doc_directories(self):
        data = '''Documents,2051,2051
Documents/seamansguide.com,322,322
Documents/seamanslog.com,405
Documents/markseaman.org,19
Documents/markseaman.info,65
Documents/shrinking-world.com,548
Documents/shrinking-world.io,59
Documents/shrinking-world.org,3
Documents/spiritual-things.org,431
Documents/SHRINKING-WORLD-PUBS,184
'''
        for x in list(reader(data.splitlines())):
            # print(x)
            if x[2:]:
                self.assertFiles(x[0], int(x[1]), int(x[2]))
            else:
                self.assertFiles(x[0], int(x[1]), int(x[1]))
