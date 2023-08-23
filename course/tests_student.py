from datetime import datetime
from course.course import bacs350_options, create_course, cs350_options

from probe.tests_django import DjangoTest

from .student import create_student, export_students, import_students, list_students, students
from .models import Student


class StudentModelTest(DjangoTest):

    def setUp(self):
        self.course1 = create_course(**cs350_options())
        self.course2 = create_course(**bacs350_options())

    def test_student_add(self):
        student = create_student(name='Test Student', course='cs350')
        self.assertEqual(len(students()), 1)
        self.assertEqual(student.user.username, 'TestStudent')
        self.assertEqual(student.user.first_name, 'Test')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'TestStudent@shrinking-world.com')

    def test_duplicate(self):
        create_student(name='Test Student', email='new_email@me.us',
                       user__last_name="Seaman", course='cs350')
        student = create_student(name='Test Student', course='cs350')
        self.assertEqual(len(students()), 1)
        self.assertEqual(student.user.username, 'TestStudent')
        self.assertEqual(student.user.first_name, 'Test')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'new_email@me.us')

    def test_multiple(self):
        create_student(name='Test Student',
                       email='x1@me.us', course='cs350')
        create_student(name='Test Student2',
                       email='x2@me.us', course='cs350')
        self.assertEqual(len(students()), 2)
        student = Student.objects.get(id=2)
        self.assertEqual(student.user.last_name, 'Student2')
        self.assertEqual(student.user.email, 'x2@me.us')
        student = Student.objects.get(id=1)
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'x1@me.us')

    def test_import(self):
        x = import_students('students.csv')
        self.assertEqual(len(students(course__name='cs350')), 12)
        self.assertEqual(len(students(course__name='bacs350')), 4)

    def test_list_students(self):
        x = import_students('students.csv')
        # for s in list_students():
        #     print(s)
        self.assertEqual(len(list_students()), 16)

    def test_export(self):
        import_students('students.csv')
        export_students('./students2.csv')
