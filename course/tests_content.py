from django.test import TestCase

from .course import cs350_options, bacs350_options, create_course
from .import_export import import_all_courses
from .models import Content, Course


class CourseDataTest(TestCase):
    def setUp(self):
        # self.user, self.user_args = create_test_user()
        self.course = create_course(**bacs350_options())

    def test_add_content(self):
        self.assertEqual(len(Content.objects.all()), 0)

        data = dict(
            course=self.course, order="1", folder=None, title="Title", doctype="Lesson"
        )
        Content.objects.create(**data)

    def test_import(self):
        import_all_courses()
        self.assertEqual(len(Content.objects.all()), 163)
