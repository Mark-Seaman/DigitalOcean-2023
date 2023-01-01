from django.test import TestCase

from task.models import Task
from task.task import task_import_files


class TaskDataTest(TestCase):

    def setUp(self):
        self.task1 = dict(name='Work')
        self.task2 = dict(name='Play', hours=10)

    def test_add_book(self):
        self.assertEqual(len(Task.objects.all()), 0)
        Task.objects.create(**self.task1)
        Task.objects.create(**self.task2)
        x = Task.objects.get(pk=2)
        # self.assertEqual(str(x), '')
        self.assertEqual(x.name, 'Play')
        self.assertEqual(x.hours, 10)
        self.assertEqual(len(Task.objects.all()), 2)

    # def test_task_import(self):
    #     task_import_files(100)
    #     tasks = Task.objects.all()
    #     self.assertGreater(len(tasks), 422)

