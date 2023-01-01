from django.test import TestCase

from probe.models import Probe


class TestDataTest(TestCase):

    def setUp(self):
        self.test1 = dict(name='Files list', expected='Initial output 1', source='test.test_system.test_system_source')
        self.test2 = dict(name='Python code', expected='Initial output 2', source='test.test_system.test_python_source')

    def test_add_test(self):
        self.assertEqual(len(Probe.objects.all()), 0)
        Probe.create(**self.test1)
        x = Probe.objects.get(pk=1)
        self.assertEqual(x.source, self.test1['source'])
        self.assertEqual(len(Probe.objects.all()), 1)

    def test_test_edit(self):
        Probe.create(**self.test1)
        b = Probe.objects.get(pk=1)
        b.expected = self.test2['expected']
        b.source = self.test2['source']
        b.save()
        self.assertEqual(b.expected, self.test2['expected'])

    def test_test_delete(self):
        Probe.objects.create(**self.test1)
        b = Probe.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Probe.objects.all()), 0)

