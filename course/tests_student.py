from django.contrib.auth import authenticate

from probe.tests_django import DjangoTest

from .student import create_student, list_students, students
from .models import Student


class StudentModelTest(DjangoTest):

    fixtures = ['config/data.json']

    def test_student_add(self):
        student = create_student(name='Test Student', course='cs350')
        self.assertEqual(len(students()), 37)
        self.assertEqual(student.user.username, 'TestStudent')
        self.assertEqual(student.user.first_name, 'Test')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'TestStudent@shrinking-world.com')

    def test_duplicate(self):
        create_student(name='Test Student', email='new_email@me.us',
                       user__last_name="Seaman", course='cs350')
        student = create_student(name='Test Student', course='cs350')
        self.assertEqual(len(students()), 37)
        self.assertEqual(student.user.username, 'TestStudent')
        self.assertEqual(student.user.first_name, 'Test')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'TestStudent@shrinking-world.com')

    def test_multiple(self):
        create_student(name='Test Student',
                       email='x1@me.us', course='cs350')
        create_student(name='Test Student2',
                       email='x2@me.us', course='cs350')
        self.assertEqual(len(students()), 38)
        student = Student.objects.get(user__email='x2@me.us')
        self.assertEqual(student.user.last_name, 'Student2')
        self.assertEqual(student.user.email, 'x2@me.us')
        student = Student.objects.get(user__email='x1@me.us')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'x1@me.us')

    def test_import_students(self):
        self.assertEqual(len(students()), 36)
        self.assertEqual(len(list_students('cs350')), 18)
        self.assertEqual(len(list_students('bacs350')), 18)
        self.assertEqual(len(students(course__name='cs350')), 18)
        self.assertEqual(len(students(course__name='bacs350')), 18)

    def test_students(self):
        self.assertEqual(len(students()), 36)
        self.assertEqual(len(students(course__name='cs350')), 18)
        self.assertEqual(len(students(course__name='bacs350')), 18)

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
        s = Student.objects.get(
            user__username='RyanLunas', course__name='cs350')
        a = authenticate(username=s.user.username, password='UNC')
        self.assertEqual(a, s.user)
        self.assertNotEqual(s.user.password, 'UNC')
        # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')

    def test_email_login(self):
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')

        self.assertEqual(s.name, 'Ryan Lunas')
        self.assertEqual(s.user.check_password('UNC'), True)
        # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')

    def login(self):
        response = self.client.login(
            username=self.user.username,  password=self.user_args['password'])
        self.assertEqual(response, True)

    def test_course_view(self):
        response = self.client.get('/course')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.url, reverse('course_list'))

    def test_bacs350(self):
        url = '/course/bacs350'
        response = self.client.get(url)
        # print(reverse('course_index', {'course': 'bacs350'}))
        # self.assertEqual('course_index', reverse(url))
        self.assertEqual(response.status_code, 200)
