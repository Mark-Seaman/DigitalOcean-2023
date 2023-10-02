from io import StringIO
from pathlib import Path
from django.core.management import call_command
from django.test import TestCase
from course.student import import_students

from course.workspace import workspace_path
from publish.import_export import load_json_data, save_json_data

from .course import bacs350_options, create_course
from .import_export import import_all_courses
from .models import Content, Student


class CourseDataTest(TestCase):
    def setUp(self):
        self.course = create_course(**bacs350_options())

    def test_add_content(self):
        self.assertEqual(len(Content.objects.all()), 0)

        data = dict(
            course=self.course, order="1", folder=None, title="Title", doctype="Lesson"
        )
        Content.objects.create(**data)

    def test_create_fixture(self):
        import_all_courses()
        self.assertEqual(len(Content.objects.all()), 163)
        text = save_json_data('config/course.json', 'course')
        self.assertEqual(len(text), 45105)

        s = workspace_path(course='bacs350', project='_students.csv')
        import_students(s)
        text = save_json_data('config/data.json')
        self.assertEqual(len(text), 87046)

    def test_load_fixture(self):
        text = load_json_data('config/data.json')
        self.assertEqual(text, 'Installed 318 object(s) from 1 fixture(s)\n')
        self.assertEqual(len(Content.objects.all()), 163)
        self.assertEqual(len(Student.objects.all()), 36)
