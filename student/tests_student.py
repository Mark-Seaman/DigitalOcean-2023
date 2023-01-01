import re
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from course.course import bacs350_options, create_course
from .models import Student


def user_args():
    return dict(username='seaman', email='test@test.us', password='secret')


def test_user():
    return get_user_model().objects.create_user(**user_args())


class StudentDataTest(TestCase):

    def setUp(self):
        self.user = test_user()
        self.course = create_course(**bacs350_options())
        self.student = dict(user=self.user, course=self.course)

    def test_add(self):
        self.assertEqual(len(Student.objects.all()), 0)
        Student.objects.create(**self.student)
        x = Student.objects.get(pk=1)
        self.assertEqual(x.name, ' ')
        self.assertEqual(x.course.name, 'bacs350')
        self.assertEqual(len(Student.objects.all()), 1)
    
    def test_edit(self):
        Student.objects.create(**self.student)
        x = Student.objects.get(pk=1)
        x.user.first_name = 'Unknown'
        x.user.last_name = 'User'
        x.user.save()
        self.assertEqual(x.name, 'Unknown User')
        self.assertEqual(len(Student.objects.all()), 1)
    
    def test_delete(self):
        Student.objects.create(**self.student)
        b = Student.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Student.objects.all()), 0)


class StudentViewsTest(TestCase):

    def login(self):
        username = self.user.username
        password = user_args()['password']
        response = self.client.login(username=username, password=password)
        self.assertEqual(response, True)

    def setUp(self):
        self.user = test_user()
        self.course = create_course(**bacs350_options())
        self.student = dict(user=self.user, course=self.course)

    def test_student_home(self):
        response = self.client.get('/course/bacs350/home')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/course/bacs350')

    def test_student_list_view(self):
        Student.objects.create(**self.student)
        response = self.client.get('/course/bacs350/student/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/list.html')
        self.assertTemplateUsed(response, 'student/_students.html')
        self.assertTemplateUsed(response, 'theme.html')
        self.assertTemplateUsed(response, '_course_navbar.html')
        self.assertContains(response, '<tr>', count=2)
    
    def test_student_detail_view(self):
        Student.objects.create(**self.student)
        url = reverse('student_detail', args=('bacs350','1'))
        self.assertEqual(url, '/course/bacs350/student/1')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'student/detail.html')
        self.assertContains(response, '<body>')
    
    def test_student_home_view(self):
    
        # Test without Login
        url = reverse('student_view', args=('bacs350',))
        self.assertEqual(url, '/course/bacs350/home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/course/bacs350')
        self.assertEqual(len(Student.objects.all()), 0)

        # Test with Login
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/course/bacs350/student/1/')
        self.assertEqual(len(Student.objects.all()), 1)

        x = Student.objects.get(pk=1)
        self.assertEqual(x.name, ' ')
       
    def test_student_edit_view(self):
    
        # Edit without Login
        Student.objects.create(**self.student)
        url = reverse('student_edit', args=('bacs350','1'))
        self.assertEqual(url, '/course/bacs350/student/1/')
        data = dict(github='http://google.com', server='http://google.com')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/course/bacs350/student/1/')

        # Test with Login
        self.login()
        url = reverse('student_edit', args=('bacs350', '1'))
        data = dict(github='http://google.com/github', server='http://google.com/server')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertContains(response, 'http://google.com/github')
        self.assertContains(response, 'http://google.com/server')

        # Check the object
        s = Student.objects.get(pk=1)
        self.assertEqual(s.server, 'http://google.com/server')

    def test_student_delete_view(self):
        Student.objects.create(**self.student)
        self.assertEqual(len(Student.objects.all()), 1)
        self.login()
        self.assertEqual(reverse('student_delete', args=['bacs350', '1']), '/course/bacs350/student/1/delete')
        response = self.client.post('/course/bacs350/student/1/delete')
        self.assertEqual(len(Student.objects.all()), 0)
