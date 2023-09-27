from io import StringIO
from pathlib import Path
from django.core.management import call_command
from django.test import TestCase
from course.student import import_students

from course.workspace import workspace_path

from .course import bacs350_options, create_course
from .import_export import import_all_courses
from .models import Content


def save_json_data(file, app=None):
    output = StringIO()
    if app:
        call_command('dumpdata', app, stdout=output, indent=4)
    else:
        call_command('dumpdata', stdout=output, indent=4)
    text = output.getvalue()
    output.close()
    Path(file).write_text(text)
    return text


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
        text = save_json_data('config/course.json')
        self.assertEqual(len(text), 55458)

    def test_load_fixture(self):
        output = StringIO()
        call_command('loaddata', 'config/course.json', stdout=output)
        self.assertEqual(len(Content.objects.all()), 163)
        self.assertEqual(
            output.getvalue(), 'Installed 165 object(s) from 1 fixture(s)\n')
