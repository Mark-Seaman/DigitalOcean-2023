from django.test import TestCase

from publish.import_export import load_json_data, save_json_data

from .import_export import import_all_courses
from .models import Content, Student
from .student import import_students
from .workspace import workspace_path


class CourseDataTest(TestCase):

    def test_create_fixture(self):
        import_all_courses()
        self.assertEqual(len(Content.objects.all()), 163)
        s = workspace_path(course='bacs350', project='_students.csv')
        import_students(s)
        text = save_json_data('config/data.json')
        self.assertEqual(len(text), 86210)

    def test_load_fixture(self):
        text = load_json_data('config/data.json')
        self.assertEqual(text, 'Installed 316 object(s) from 1 fixture(s)\n')
        self.assertEqual(len(Content.objects.all()), 163)
        self.assertEqual(len(Student.objects.all()), 35)
