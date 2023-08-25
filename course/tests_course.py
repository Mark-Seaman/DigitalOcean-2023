from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from publish.text import text_join

from .course import create_courses, cs350_options, bacs350_options, create_course, find_artifacts
from .import_export import import_all_courses
from .models import Course, Student
from .student import import_students, students


class CourseDataTest(TestCase):
    def setUp(self):
        self.course1 = cs350_options()
        self.course2 = bacs350_options()

    def test_add_course(self):
        self.assertEqual(len(Course.objects.all()), 0)
        create_course(**self.course1)
        create_course(**self.course2)
        x = Course.objects.get(pk=2)
        self.assertEqual(
            str(x), "2 - bacs350 - UNC BACS 350 - Web Apps with Python")
        self.assertEqual(x.title, "UNC BACS 350 - Web Apps with Python")
        self.assertEqual(len(Course.objects.all()), 2)

    def test_course_edit(self):
        create_course(**self.course1)
        b = Course.objects.get(pk=1)
        b.title = self.course2["title"]
        b.description = self.course2["description"]
        b.save()
        self.assertEqual(b.title, self.course2["title"])
        self.assertEqual(b.description, self.course2["description"])

    def test_course_delete(self):
        create_course(**self.course1)
        b = Course.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Course.objects.all()), 0)

    def test_course_artifacts(self):
        import_all_courses()
        items = find_artifacts('cs350')
        self.assertEqual(len(items), 88)
        items = find_artifacts('bacs350')
        # print(text_join(items))
        self.assertEqual(len(items), 98)

    def test_create_courses(self):
        create_courses()
        create_courses()
        self.assertEqual(len(Course.objects.all()), 2)  # don't duplicate


class CourseViewsTest(TestCase):
    def login(self):
        response = self.client.login(
            username=self.user.username, password=self.user_args["password"]
        )
        self.assertEqual(response, True)

    def setUp(self):
        # self.user, self.user_args = create_test_user()
        self.course1 = cs350_options()
        self.course2 = bacs350_options()

    def test_course_list_view(self):
        self.assertEqual(reverse("course_list"), "/course")
        create_course(**self.course1)
        create_course(**self.course2)
        response = self.client.get("/course")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course_list.html")
        self.assertTemplateUsed(response, "course_theme.html")
        self.assertContains(response, "<tr>", count=3)

    def test_course_detail_view(self):
        self.assertEqual(reverse("course_index", args=[
                         "bacs200"]), "/course/bacs200")
        self.assertEqual(reverse("course_index", args=[
                         "bacs350"]), "/course/bacs350")
        create_course(**self.course2)
        response = self.client.get(reverse("course_index", args=["bacs350"]))
        self.assertContains(response, "Python Web Apps")

    def test_course_build(self):
        import_all_courses(verbose=False)


# class CourseFixtureTest(TestCase):
#
#     def test_import_courses(self):
#         self.user, self.user_args = create_test_user()
#         import_all_courses()
#         self.assertEqual(len(Author.objects.all()), 2)
#         self.assertEqual(len(Course.objects.all()), 2)
#         self.assertEqual(len(Lesson.objects.all()), 90)
