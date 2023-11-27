from pathlib import Path

from course.models import Content
from probe.tests_django import DjangoTest
from publish.files import concatonate

from .models import Content, Pub
from .publication import all_blogs, all_books, all_privates, all_pubs


# -----------------------
# Pub Data Model

class PubDataTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_blog_add(self):
        blog1 = Pub.objects.create(
            name="Write", title="Authoring Tips", url="write")
        blog2 = Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        self.assertEqual(len(Pub.objects.all()), 22)

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

    def test_with_data(self):
        num = len(Content.objects.all())
        self.assertRange(num, 1300, 1400, "Content objects")

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
        self.assertNumLines(text, 3200, 3400)

    def test_pub_list(self):
        pubs = ', '.join([p.name for p in all_pubs()])
        self.assertEqual(len(all_pubs()), 20)
        names = 'ai, family, ghost, io, journey, leverage, marks, org, poem, private, quest, sampler, spiritual, spirituality, sweng, tech, today, webapps, write, stacie'
        self.assertEqual(pubs, names)
