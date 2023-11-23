from pathlib import Path

from django.test import TestCase
from requests import get

from publish.files import read_file
from publish.text import line_count, text_lines

INTERNET_DISABLED = False


class DjangoTest(TestCase):

    def assertFiles(self, directory, min, max):
        num_files = len([f for f in Path(directory).rglob("*.md")])
        error = f"files in {directory}: {num_files} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num_files, min, error)
        self.assertLessEqual(num_files, max, error)

    def assertPage(self, page):
        if page.startswith('/'):
            response = self.client.get(page)
            text = response.content.decode('utf-8')
        else:
            if INTERNET_DISABLED:
                return
            response = get(page)
            text = response.text
        self.assertEqual(response.status_code, 200)
        return text

    def assertPageLines(self, page, min, max):
        self.assertNumLines(self.assertPage(page), min, max)

    def assertPageText(self, page, min, max, pattern=None):
        text = self.assertPage(page)
        self.assertNumLines(text, min, max)
        if pattern:
            self.assertIn(pattern, text)
        return text

    def assertNumLines(self, text, min, max=1000, label='Lines of Text'):
        lines = line_count(text)
        self.assertRange(lines, min, max, label)

    def assertFileLines(self, path, min, max):
        self.assertNumLines(read_file(path), min, max)

    def assertFile(self, path):
        self.assertTrue(Path(path).exists())

    def assertRange(self, num, min, max, label="Value"):
        error = f"{label} {num} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num, min, error)
        self.assertLessEqual(num, max, error)

    def assertText(self, text, pattern):
        self.assertIn(pattern, text)

    def print_test_name(self):
        print(f'\nTest: \n{self._testMethodName}\n')
        # print(self.id().split('.')[-1])

    # def test_django_test(self):
    #     self.assertTrue(True)
