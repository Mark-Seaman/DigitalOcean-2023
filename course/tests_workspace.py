from django.urls import reverse
from course.models import Student
from course.student import import_students
from course.workspace import workspace_path
from probe.tests_django import DjangoTest

# ---------------
# Test Log
# count the number of tests & assertions
# track number of test executions for every 5 minutes
# measure time to execute one iteration and all tests
# 109 tests

# 00 oox
# 10 ooooo
# 20 ooo
# 25
# 30 oo
# 35 oo
# 40 oxxoo
# 45 oo
# 50 oo
# 55 oo


class StudentWorkspaceTest(DjangoTest):

    @classmethod
    def setUpTestData(cls):
        s = workspace_path(course='bacs350', project='_students.csv')
        import_students(s)
        # y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350/_students.csv'
        # self.assertTrue(s.exists())  # No student list
        # self.assertEqual(str(s), y)  # Student roster

    def test_workspace_exists(self):
        x = workspace_path(course='bacs350')
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350'
        self.assertEqual(str(x), y)
        self.assertTrue(x.exists())

    def test_project_exists(self):
        x = workspace_path(course='bacs350', project='01')
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350/01'
        self.assertEqual(str(x), y)
        self.assertTrue(x.exists())

    def test_doc_exists(self):
        x = workspace_path(course='bacs350', project='01', doc='Index.md')
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350/01/Index.md'
        self.assertEqual(str(x), y)
        self.assertTrue(x.exists())

    def test_student_exists(self):
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')
        self.assertEqual(s.name, 'Ryan Lunas')
        self.assertEqual(s.user.check_password('CS350'), True)

    def test_student_github(self):
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')
        self.assertEqual(s.github, 'https://github.com')  # Github repo
        self.assertEqual(s.server, 'https://digitalocean.com')  # Digital Ocean

    def test_workspace_content(self):
        c = workspace_path(course='bacs350', project='_content.csv')
        self.assertTrue(c.exists())  # Course content CSV

    def test_workspace_json(self):
        c = workspace_path(course='bacs350', project='_course.json')
        self.assertTrue(c.exists())  # Course JSON file

    def test_workspace_view(self):
        self.assertEqual(reverse("course_list"), "/course")
        response = self.client.get("/course")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course_list.html")
        self.assertTemplateUsed(response, "course_theme.html")
        self.assertContains(response, "<tr>", count=3)

    def test_workspace_edit(self):
        pass
