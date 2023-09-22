from course.team import get_page, page_path, read_page, write_page, write_team_page
from probe.tests_django import DjangoTest

from .models import Team


class TeamPagesTest(DjangoTest):

    # @classmethod
    # def setUpTestData(cls):
    #     create_courses()
    #     s = workspace_path(course='bacs350', project='_students.csv')
    #     import_students(s)

    def test_page_path(self):
        # print(page_path())
        y = 'Documents/shrinking-world.com/cs350/team'
        self.assertEqual(str(page_path()), y)
        y = 'Documents/shrinking-world.com/cs350/team/Index.md'
        self.assertEqual(str(page_path('Index.md')), y)
        x = str(page_path('Index.md', '1'))
        y = 'Documents/shrinking-world.com/cs350/team/1/Index.md'
        self.assertEqual(x, y)
        x = str(page_path('Index.md', '1', '4'))
        y = 'Documents/shrinking-world.com/cs350/team/1/4/Index.md'
        self.assertEqual(x, y)
        x = str(page_path('Index.md', '1', '4', '2'))
        y = 'Documents/shrinking-world.com/cs350/team/1/4/2/Index.md'
        self.assertEqual(x, y)

    def test_read_page(self):
        path = page_path('TeamProjects.md')
        x = read_page(path)
        self.assertEqual(len(x['html']), 223)
        self.assertEqual(x['title'], 'Team Projects')

    def test_write_page(self):
        t = Team.objects.create(name='Development Test', pk=6)
        path = page_path('TeamProject.md', str(t.pk))
        write_page(path, t)
        x = read_page(path)
        self.assertEqual(len(x['html']), 260)
        self.assertEqual(x['title'], 'Team Project Workspace')
        path.unlink()

    def test_team_page(self):
        path = page_path('TeamProject.md', '2')
        x = read_page(path)
        self.assertEqual(len(x['html']), 915)
        self.assertEqual(x['title'], 'Team Project Workspace')

    def test_write_team_page(self):
        Team.objects.create(name='Development Test', pk=6)
        x = get_page('6')
        self.assertEqual(len(x['html']), 260)
        self.assertEqual(x['title'], 'Team Project Workspace')
        x['path'].unlink()

    def test_milestone1_page(self):
        Team.objects.create(name='Development Test', pk=6,
                            github='https://github.com', server='https://digitalocean.com')
        x = get_page('6', '1')
        self.assertEqual(len(x['html']), 1950)
        y = 'Client Feedback - Development Test - Milestone 1'
        self.assertEqual(x['title'], y)
        x['path'].unlink()

    def test_milestone2_page(self):
        Team.objects.create(name='Development Test', pk=6,
                            github='https://github.com', server='https://digitalocean.com')
        x = get_page('6', '2')
        self.assertEqual(len(x['html']), 1870)
        y = 'Development Test - Milestone 2 - Technical Feasibility'
        self.assertEqual(x['title'], y)
        x['path'].unlink()

    def test_get_page(self):
        Team.objects.create(name='Development Test', pk=6)
        x = get_page('6')
        self.assertEqual(len(x['html']), 260)
        self.assertEqual(x['title'], 'Team Project Workspace')
        x['path'].unlink()

    # def test_create_team_pages(self):
    #     for t in Team.objects.all():
    #         print(t)
