from pathlib import Path

from publish.text import text_join, text_lines
from course.course import get_course
from .models import Content


def prepare_lesson(week):
    print(f'Prepare Lesson for Week {week}')
    course = get_course("bacs350")
    for c in Content.objects.filter(folder__order=week, doctype='chapter'):
        show_headings(c.document)
    for c in Content.objects.filter(folder__order=week, doctype='skill'):
        show_headings(c.document)
    for c in Content.objects.filter(folder__order=week, doctype='demo'):
        show_headings(c.document)
    for c in Content.objects.filter(folder__order=week, doctype='project'):
        show_headings(c.document)


def show_headings(path):
    print(path)
    lines = text_lines(Path(path).read_text())
    text = [t for t in lines if t.startswith('#')]
    print(text_join(text))
