from django.test import TestCase
from django.urls import reverse

from .course import create_courses, cs350_options, bacs350_options, create_course, find_artifacts
from .models import Content, Course, Student


class CourseDataTest(TestCase):
    fixtures = ['config/data.json']

    def setUp(self):
        self.course1 = cs350_options()
        self.course2 = bacs350_options()

    def test_load_fixture(self):
        self.assertEqual(len(Course.objects.all()), 2)
        self.assertEqual(len(Content.objects.all()), 163)
        self.assertEqual(len(Student.objects.all()), 36)

    def test_add_course(self):
        self.assertEqual(len(Course.objects.all()), 2)
        create_course(**self.course1)
        create_course(**self.course2)
        x = Course.objects.get(pk=1)
        self.assertEqual(
            str(x), "1 - cs350 - UNC CS 350 - Software Engineering")
        self.assertEqual(x.title, "UNC CS 350 - Software Engineering")
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
        Course.objects.get(pk=1).delete()
        self.assertEqual(len(Course.objects.all()), 1)

    def test_create_courses(self):
        create_courses()
        create_courses()
        self.assertEqual(len(Course.objects.all()), 2)  # don't duplicate

    def test_course_artifacts(self):
        items = find_artifacts('cs350')
        self.assertEqual(len(items), 88)
        items = find_artifacts('bacs350')
        # print(text_join(items))
        self.assertEqual(len(items), 100)

    def test_course_list_view(self):
        self.assertEqual(reverse("course_list"), "/course")
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
        response = self.client.get(reverse("course_index", args=["bacs350"]))
        self.assertContains(response, "Python Web Apps")

    def test_import_courses(self):
        self.assertEqual(len(Course.objects.all()), 2)
        self.assertEqual(len(Content.objects.all()), 163)

    # def test_course_view(self):
    #     self.assertEqual(reverse("course_list"), "/course")
    #     response = self.client.get("/course")
    #     self.assertEqual(response.status_code, 200)


# ---------------
# Test Log
# count the number of tests & assertions
# track number of test executions for every 5 minutes
# measure time to execute one iteration and all tests
# 114 tests

# 00 x <--
# 10 oxxo
# 20 oooo
# 30 ooo
# 40 xox
# 50 xoo
