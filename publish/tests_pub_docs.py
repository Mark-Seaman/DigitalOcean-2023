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
Documents/SHRINKING-WORLD-PUBS,184
'''
        # import pandas as pd
        # from io import StringIO

        # df = pd.read_csv(StringIO(data), header=None)
        # df[2] = df[2].fillna(df[1])
        # data = df.values.tolist()

        # for x in read_csv_text(data):
        for x in csv_to_list(data):
            self.assertFiles(x[0], int(x[1]), int(x[1]))

def read_csv_text(text):
    import pandas as pd
    from io import StringIO

    df = pd.read_csv(StringIO(text), header=None)
    df[2] = df[2].fillna(df[1])
    return df.values.tolist()
     

from csv import reader

def csv_to_list(csv_data):
    return list(reader(csv_data.splitlines()))
