from django.urls import reverse
from course.models import Student
from course.student import import_students
from course.workspace import workspace_path
from probe.tests_django import DjangoTest


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
        x = workspace_path(course='bacs350', project='1')
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350/1'
        self.assertEqual(str(x), y)
        self.assertTrue(x.exists())

    def test_doc_exists(self):
        x = workspace_path(course='bacs350', project='1', doc='Index.md')
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350/1/Index.md'
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
        w = dict(course='bacs350', project='1', doc='Index.md')
        x = str(workspace_path(**w))
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/bacs350/1/Index.md'
        self.assertEqual(x, y)
        response = self.client.get("/workspace")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workspace.html")
        self.assertTemplateUsed(response, "course_theme.html")

    def test_bacs350_view(self):
        response = self.client.get("/workspace/bacs350")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workspace.html")
        self.assertContains(response, 'Shrinking World')
        self.assertContains(response, '# BACS 350 Index')

    def test_project_view(self):
        response = self.client.get("/workspace/bacs350/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workspace.html")
        self.assertContains(response, 'Shrinking World')
        self.assertContains(response, 'Index File for Project 1')

    def test_doc_view(self):
        response = self.client.get("/workspace/bacs350/1/Index.md")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workspace.html")
        self.assertContains(response, 'Shrinking World')
        self.assertContains(response, 'Index File for Project 1')

    def test_student_info(self):
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')
        response = self.client.login(
            username=s.user.username,  password='CS350')
        response = self.client.get("/workspace/bacs350/1/Index.md")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RyanLunas')

    def test_student_failed_login(self):
        s = Student.objects.get(
            user__email='luna0500@bears.unco.edu', course__name='cs350')
        self.assertEqual(self.client.login(
            username=s.user.username,  password='x'), False)

    # def test_email_login(self):
    #     s = Student.objects.get(
    #         user__email='luna0500@bears.unco.edu', course__name='cs350')
    #     self.assertEqual(s.name, 'Ryan Lunas')
    #     self.assertEqual(s.user.check_password('CS350'), True)

    # def test_student_edit(self):
    #     pass

# ---------------
# Test Log
# count the number of tests & assertions
# track number of test executions for every 5 minutes
# measure time to execute one iteration and all tests
# 114 tests

# 00 x <--
# 10 oxxo
# 15 o
# 20 oooo
# 25 xxoo
# 30 ooo
# 35 oooxooo
# 40 xox
# 45 xoooo
# 50 xoo
# 55 ooo

    # def test_student_info(self):
    #     pass

    # def test_student_info(self):
    #     pass

        # self.assertContains(response, "<tr>", count=3)
    #     w = dict(course='bacs350', project='1', doc='Index.md')
        # self.assertEqual(reverse("workspace", w), "/workspace")

    #     # self.assertEqual(reverse("workspace", w), "/workspace")
    #     response = self.client.get("/workspace")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "workspace.html")
    #     self.assertTemplateUsed(response, "course_theme.html")
    #     # self.assertContains(response, "<tr>", count=3)

    # def test_workspace_edit(self):
    #     pass
