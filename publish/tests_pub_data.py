from pathlib import Path

from course.models import Content
from probe.tests_django import DjangoTest
from publish.files import concatonate
from publish.import_export import save_json_data

from .days import is_old
from .models import Content, Pub
from .publication import all_blogs, all_books, all_privates, all_pubs, build_pubs, show_pubs


# -----------------------
# Pub Data Model


class PubDataTest(DjangoTest):

    # Pub Data Model
    def setup(self):
        blog1 = Pub.objects.create()

    def test_blog_add(self):
        blog1 = Pub.objects.create(
            name="Write", title="Authoring Tips", url="write")
        blog2 = Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        self.assertEqual(len(Pub.objects.all()), 2)

    def test_blog_detail(self):
        Pub.objects.create(name="Write", title="Authoring Tips", url="write")
        Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        blog1 = Pub.objects.get(name="Write")
        blog2 = Pub.objects.get(title="Pro Pub", url="tech")
        self.assertEqual(blog1.title, "Authoring Tips")
        self.assertEqual(blog1.url, "write")
        self.assertEqual(blog2.url, "tech")

    def test_blog_edit(self):
        Pub.objects.create(name="Write", title="Authoring Tips", url="write")
        Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        blog1 = Pub.objects.get(name="Write")
        blog2 = Pub.objects.get(title="Pro Pub", url="tech")
        blog1.title = "New Tips"
        blog1.url = "newurl"
        self.assertEqual(blog1.title, "New Tips")
        self.assertEqual(blog1.url, "newurl")
        self.assertEqual(blog2.url, "tech")


# -----------------------
# Pub Fixture

class FixtureTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_with_data(self):
        num = len(Content.objects.all())
        self.assertRange(num, 213, 1400, "Content objects")

    def test_pub_list(self):
        self.assertRange(len(all_pubs()), 20, 24, 'Num Pubs')

    def test_book_list(self):
        self.assertRange(len(all_books()), 3, 5, 'Num Book Pubs')

    def test_blog_list(self):
        self.assertRange(len(all_blogs()), 0, 9, 'Num Blog Pubs')

    def test_private_list(self):
        self.assertRange(len(all_privates()), 1, 9, 'Num Private Pubs')

    def test_images(self):
        self.assertRange(
            len(list(Path('static/images').glob('**'))), 39, 45, 'Images in Static')

    def test_pub_info(self):
        text = concatonate('publish/*.py')
        self.assertNumLines(text, 3000, 3200)

    def test_rebuld_pubs(self):
        if is_old("config/publish.json"):
            print('config/publish is old')
            build_pubs(delete=True)
            self.assertRange(len(Pub.objects.all()), 20, 20)
            self.assertRange(len(Content.objects.all()),
                             1200, 1300, "Content Nodes")
            text = save_json_data('config/publish.json')
            self.assertEqual(len(text), 456548)

    def test_data_file(self):
        self.assertFalse(is_old("config/publish.json"),
                         'config/publish.json is old')

    def test_pub_list(self):
        pubs = ', '.join([p.name for p in all_pubs()])
        self.assertEqual(len(all_pubs()), 20)
        names = 'ai, cellbiology, family, ghost, io, journey, leverage, marks, org, poem, private, quest, sampler, spiritual, spirituality, sweng, tech, today, webapps, write'
        self.assertEqual(pubs, names)

    def test_sweng(self):
        journey = show_pubs('journey')
        x = 'journey         -  A Seaman\'s Journey                  - 66160 words - 264 pages'
        self.assertEqual(journey, x)
        sweng = show_pubs('sweng')
        x = 'sweng           -  Software Engineering with AI        -  7526 words - 30 pages'
        self.assertEqual(sweng, x)
