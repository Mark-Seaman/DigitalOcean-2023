from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password
from datetime import datetime
from course.course import bacs350_options, create_course, create_courses, cs350_options

from probe.tests_django import DjangoTest

from .student import create_student, export_students, import_students, list_students, students
from .models import Student


class StudentModelTest(DjangoTest):

    def setUp(self):
        create_courses()

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

    def test_export_students(self):
        import_students('students.csv')
        export_students('./students2.csv')

    def test_import_students(self):
        import_students('students2.csv')
        self.assertEqual(len(students()), 27)
        self.assertEqual(len(students(course__name='cs350')), 13)
        self.assertEqual(len(students(course__name='bacs350')), 14)
        self.assertEqual(len(list_students()), 27)

    def test_students(self):
        import_students('students2.csv')
        s1 = Student.objects.get(
            user__username='RyanLunas', course__name='cs350')
        self.assertEqual(s1.name, 'Ryan Lunas')
        self.assertEqual(s1.course.name, 'cs350')
        s2 = Student.objects.get(
            user__username='RyanLunas', course__name='bacs350')
        self.assertEqual(s2.name, 'Ryan Lunas')
        self.assertEqual(s2.course.name, 'bacs350')
        self.assertEqual(s1.user.email, 'luna0500@bears.unco.edu')
        self.assertEqual(s2.user.email, 'luna0500@bears.unco.edu')

    def test_students(self):
        import_students('students2.csv')
        self.assertEqual(len(students()), 27)
        self.assertEqual(len(students(course__name='cs350')), 13)
        self.assertEqual(len(students(course__name='bacs350')), 14)

        s1 = Student.objects.get(
            user__username='RyanLunas', course__name='cs350')
        self.assertEqual(s1.name, 'Ryan Lunas')
        self.assertEqual(s1.course.name, 'cs350')
        s2 = Student.objects.get(
            user__username='RyanLunas', course__name='bacs350')
        self.assertEqual(s2.name, 'Ryan Lunas')
        self.assertEqual(s2.course.name, 'bacs350')
        self.assertEqual(s1.user.email, 'luna0500@bears.unco.edu')
        self.assertEqual(s2.user.email, 'luna0500@bears.unco.edu')

    def test_student_login(self):
        import_students('students2.csv')
        s = Student.objects.get(
            user__username='RyanLunas', course__name='cs350')
        # s.user.password = make_password('CS350')
        # s.user.save()
        a = authenticate(username=s.user.username, password='CS350')
        self.assertEqual(a, s.user)
        self.assertNotEqual(s.user.password, 'CS350')
        # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')

    def test_email_login(self):
        import_students('students2.csv')
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')
        # s.user.password = make_password('CS350')
        # s.user.save()
        self.assertEqual(s.name, 'Ryan Lunas')
        self.assertEqual(s.user.check_password('CS350'), True)
        # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')
