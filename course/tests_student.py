from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password
from datetime import datetime

from django.urls import reverse
from course.course import bacs350_options, create_course, create_courses, cs350_options
from course.workspace import workspace_path

from probe.tests_django import DjangoTest

from .student import create_student, export_students, import_students, list_students, students
from .models import Student


class StudentModelTest(DjangoTest):

    @classmethod
    def setUpTestData(cls):
        s = workspace_path(course='bacs350', project='_students.csv')
        import_students(s)

    def test_student_add(self):
        student = create_student(name='Test Student', course='cs350')
        self.assertEqual(len(students()), 28)
        self.assertEqual(student.user.username, 'TestStudent')
        self.assertEqual(student.user.first_name, 'Test')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'TestStudent@shrinking-world.com')

    def test_duplicate(self):
        create_student(name='Test Student', email='new_email@me.us',
                       user__last_name="Seaman", course='cs350')
        student = create_student(name='Test Student', course='cs350')
        self.assertEqual(len(students()), 28)
        self.assertEqual(student.user.username, 'TestStudent')
        self.assertEqual(student.user.first_name, 'Test')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'new_email@me.us')

    def test_multiple(self):
        create_student(name='Test Student',
                       email='x1@me.us', course='cs350')
        create_student(name='Test Student2',
                       email='x2@me.us', course='cs350')
        self.assertEqual(len(students()), 29)
        student = Student.objects.get(user__email='x2@me.us')
        self.assertEqual(student.user.last_name, 'Student2')
        self.assertEqual(student.user.email, 'x2@me.us')
        student = Student.objects.get(user__email='x1@me.us')
        self.assertEqual(student.user.last_name, 'Student')
        self.assertEqual(student.user.email, 'x1@me.us')

    def test_export_students(self):
        export_students('./students2.csv')

    def test_import_students(self):
        self.assertEqual(len(students()), 27)
        self.assertEqual(len(students(course__name='cs350')), 13)
        self.assertEqual(len(students(course__name='bacs350')), 14)
        self.assertEqual(len(list_students()), 27)

    def test_students(self):
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
        s = Student.objects.get(
            user__username='RyanLunas', course__name='cs350')
        a = authenticate(username=s.user.username, password='CS350')
        self.assertEqual(a, s.user)
        self.assertNotEqual(s.user.password, 'CS350')
        # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')

    def test_email_login(self):
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')
        self.assertEqual(s.name, 'Ryan Lunas')
        self.assertEqual(s.user.check_password('CS350'), True)
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

    # @classmethod
    # def setUpTestData(cls):
    #     s = workspace_path(course='bacs350', project='_students.csv')
    #     import_students(s)

    # def setUp(self):
    #     self.user = create_prometa_user(username='Tester')
    #     self.user1 = dict(title='Doc Title 1', body='Doc Body 1')
    #     self.user2 = dict(title='Doc Title 2', body='Doc Body 2')

    # def test_import_of_users(self):
    #     x = import_users('data/users.csv')
    #     self.assertEqual(
    #         x, 'data/users.csv: 243 records imported (Skipped 0)\n')

    # def test_login(self):
    #     self.assertFalse('TODO: user login')

    # def test_login_with_email(self):
    #     self.assertFalse('TODO: user login with email address')

    # def test_export_with_email(self):
    #     self.assertFalse('TODO: export with name, username, email, roles')

    # def test_page_security(self):
    #     self.assertFalse('TODO: page redirect based on user security')

    # def test_user_list_view(self):
    #     self.assertEqual(reverse('user_list'), '/user/')
    #     PrometaUser.objects.create(**self.user1)
    #     PrometaUser.objects.create(**self.user2)
    #     response = self.client.get('/user/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'user_list.html')
    #     self.assertTemplateUsed(response, 'theme.html')
    #     self.assertContains(response, '<tr>', count=3)
    #
    # def test_user_detail_view(self):
    #     PrometaUser.objects.create(**self.user1)
    #     self.assertEqual(reverse('user_detail', args='1'), '/user/1')
    #     self.assertEqual(reverse('user_detail', args='2'), '/user/2')
    #     response = self.client.get(reverse('user_detail', args='1'))
    #     self.assertContains(response, 'body')
    #
    # def test_user_add_view(self):
    #
    #     # Add without Login
    #     response = self.client.post(reverse('user_add'), self.user1)
    #     response = self.client.post(reverse('user_add'), self.user2)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, '/accounts/login/?next=/user/add')
    #
    #     # Login to add
    #     self.login()
    #     response = self.client.post(reverse('user_add'), self.user1)
    #     response = self.client.post(reverse('user_add'), self.user2)
    #     self.assertEqual(response.status_code, 302)
    #     response = self.client.get(response.url)
    #     self.assertEqual(len(PrometaUser.objects.all()), 2)
    #
    # def test_user_edit_view(self):
    #
    #     # Edit without Login
    #     response = PrometaUser.objects.create(**self.user1)
    #     response = self.client.post(reverse('user_edit', args='1'), self.user2)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, '/accounts/login/?next=/user/1/')
    #
    #     # Login to edit
    #     self.login()
    #     response = self.client.post('/user/1/', self.user2)
    #     self.assertEqual(response.status_code, 302)
    #     response = self.client.get(response.url)
    #     user = PrometaUser.objects.get(pk=1)
    #     self.assertEqual(user.title, self.user2['title'])
    #     self.assertEqual(user.body, self.user2['body'])
    #
    # def test_user_delete_view(self):
    #     self.login()
    #     PrometaUser.objects.create(**self.user1)
    #     self.assertEqual(reverse('user_delete', args='1'), '/user/1/delete')
    #     response = self.client.post('/user/1/delete')
    #     self.assertEqual(len(PrometaUser.objects.all()), 0)
