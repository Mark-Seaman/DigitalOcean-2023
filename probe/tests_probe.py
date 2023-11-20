import subprocess
from pathlib import Path
from sys import version_info

from django.test import TestCase
from probe.models import Probe


class TestDataTest(TestCase):

    def setUp(self):
        self.test1 = dict(name='Files list', expected='Initial output 1',
                          source='test.test_system.test_system_source')
        self.test2 = dict(name='Python code', expected='Initial output 2',
                          source='test.test_system.test_python_source')

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


class PythonEnvironmentTest(TestCase):
    def test_python_environment(self):
        requirements = '''aiohttp==3.8.5
aiosignal==1.3.1
asgiref==3.7.2
async-timeout==4.0.3
attrs==23.1.0
autopep8==2.0.4
beautifulsoup4==4.12.2
black==23.9.1
certifi==2023.7.22
charset-normalizer==3.2.0
click==8.1.7
dj-database-url==2.1.0
Django==4.2.5
django-countries==7.5.1
django-crispy-forms==1.14.0
django-extensions==3.2.3
Faker==19.6.1
frozenlist==1.4.0
gunicorn==21.2.0
idna==3.4
importlib-metadata==6.8.0
Markdown==3.4.4
multidict==6.0.4
mypy-extensions==1.0.0
numpy==1.26.0
openai==0.28.0
packaging==23.1
pandas==2.1.0
pathspec==0.11.2
Pillow==10.0.1
platformdirs==3.10.0
psycopg2-binary==2.9.7
pycodestyle==2.11.0
python-dateutil==2.8.2
python-dotenv==1.0.0
pytz==2023.3.post1
requests==2.31.0
six==1.16.0
soupsieve==2.5
sqlparse==0.4.4
tabulate==0.9.0
toml==0.10.2
tomli==2.0.1
tomlkit==0.12.1
toot==0.38.1
tqdm==4.66.1
typing_extensions==4.7.1
tzdata==2023.3
Unidecode==1.3.6
urllib3==2.0.4
urwid==2.1.2
wcwidth==0.2.6
whitenoise==6.5.0
yarl==1.9.2
zipp==3.16.2
'''
        self.assertEqual(Path('requirements.txt').read_text(), requirements)

    def test_python_packages(self):
        expected_packages = [
            'Django',
            'requests',
            'numpy',
        ]
        process = subprocess.Popen(['pip', 'freeze'], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        installed_packages = output.decode('utf-8')
        # installed_packages = output.decode('utf-8').strip().split('\n')
        for package in expected_packages:
            self.assertIn(package, installed_packages)

    def test_python_version(self):
        v = version_info[:2]
        # print('Python Version: ', v)
        self.assertTrue(v == (3, 11) or v == (3, 10))
