from probe.data import load_json_data, save_json_data
from probe.tests_django import DjangoTest
from publish.days import is_old

from .import_export import import_all_courses
from .models import Content, Student
from .student import import_students
from .workspace import workspace_path
from .models import Content


class CourseDataTest(DjangoTest):

    def test_create_fixture(self):
        if is_old("config/course.json"):
            print('data.json is old')
            import_all_courses()
            self.assertEqual(len(Content.objects.all()), 163)
            s = workspace_path(course='bacs350', project='_students.csv')
            import_students(s)
            text = save_json_data('config/course.json')
            self.assertEqual(len(text), 86210)

    def test_load_fixture(self):
        text = load_json_data('config/course.json')
        self.assertEqual(text, 'Installed 316 object(s) from 1 fixture(s)\n')
        self.assertEqual(len(Content.objects.all()), 163)
        self.assertEqual(len(Student.objects.all()), 35)
