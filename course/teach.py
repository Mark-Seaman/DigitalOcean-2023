from os import system
from pathlib import Path

from course.lesson import show_headings


def teaching_prep(command):
    print(command)
    # print(f"teaching: {command}")
    if not command:
        # lesson_outline()
        demo_outline()
    elif Path(command[0]).exists():
        system(f'code {command[0]}')
    elif command[0] == 'lesson':
        lesson_outline(command[1])
    elif command[0] == 'outline':
        outline(command[1])
    elif command[0] == 'notes':
        notes_outline()
    elif command[0] == 'demo':
        demo_outline()
    elif command[0] == 'old':
        old_lesson_outline(command[1])
    else:
        print('usage: teach [lesson|notes|demo|old]')


def demo_outline():
    text = 'Demo Outline\n\n'
    demo_path = Path('Documents/Github/WebApps-1')
    for f in sorted(demo_path.glob('*/Index.md')):
        text += show_headings(f) + '\n\n'
    outline = Path(
        f'Documents/shrinking-world.com/webapps1/outline/Demos.ol')
    outline.write_text(text)
    system(f'code {demo_path} {outline}')


def lesson_outline(doc):
    print('Lesson Outline')
    path = Path(f'Documents/shrinking-world.com/bacs350/{doc}.md')
    print(show_headings(path))


def notes_outline():
    text = 'Notes Outline\n\n'
    path = Path('Documents/shrinking-world.com/webapps1/lesson')
    for f in sorted(path.glob('??.md')):
        text += show_headings(f) + '\n\n'
    outline = Path(f'Documents/shrinking-world.com/webapps1/outline/Notes.ol')
    outline.write_text(text)
    system(f'code {path} {outline}')


def outline(doc):
    print(f'Outline - {doc}')
    print(show_headings(Path(doc)))


def old_lesson_outline(doc):
    print('Old Lesson Outline')
    path = Path(f'Documents/shrinking-world.com/bacs350/{doc}.md')
    x = 'project'
    outline = Path(
        f'Documents/shrinking-world.com/webapps1/outline/{x}.ol')
    save_outline(path, outline)
    system(f'code {path} {outline}')


def save_outline(f1, f2):
    print(f1, f2)
    text = show_headings(f1)
    f2.write_text(text)
