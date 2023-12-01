from pathlib import Path
from django.contrib.auth.models import User

import webbrowser

from course.course import initialize_course_data
from course.models import Team
from course.team import setup_team_pages, setup_teams
from publish.publication import build_pubs
from publish.text import text_join, text_lines
from task.task import fix_tasks, task_command
from task.todo import edit_todo_list
from writer.outline import create_outlines
from writer.pub_script import pub_path, pub_script
from writer.words import measure_pub_words
from publish.note import create_moderators

from .data import load_json_data, save_json_data


def quick_test():
    # print("No quick test defined")
    course()
    # create_moderators()
    # pub()
    # tasks()
    # tests()
    # writer()
    return 'OK'


def course():
    Team.objects.all().delete()
    initialize_course_data(delete=False, verbose=True, sales=False)
    setup_teams()
    setup_team_pages()


def pub():
    # Build Pubs
    build_pubs(verbose=False, delete=False)
    text = measure_pub_words()
    print(text)


def writer():
    # text = pub_script(
    #         'outline', ['ghost', 'Micropublishing', 'C-Outline.md'])
    # print(text)
    create_outlines(pub_path('sweng', 'Milestone-6'))

    # print(f'Words {pub.name}: {pub.words}')

    # pub = get_pub(x)
    # # pub.delete()
    # # create_pub(x, f'Documents/Shrinking-World-Pubs/{x}/Pub', False)
    # # create_pub_index(pub, get_pub_contents(pub))
    #
    # print(show_pub_details(pub))

    # Create Cover Images
    # path = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/poem/Images/Cover.png'
    # scale_image(path, 1600, 2560)
    # create_cover_images(path)


def tasks():
    fix_tasks()
    task_command(['week'])


def execute_pub_script(text):
    return text_join([pub_script(line.strip().split(' ')) for line in text_lines(text) if line.strip()])


def todo():
    print("TODO")
    edit_todo_list()


def write_webapps_contents():
    csv = ""
    x = 1
    for i, row in enumerate(range(14)):
        chapter = i + 1
        csv += f"chapter/{i+1:02}.md,{chapter}\n"
        x += 1
        csv += f"skill/{i*3+1:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"skill/{i*3+2:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"skill/{i*3+3:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"demo/{i+1:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"project/{i+1:02}.md,{chapter},{x}\n"
        x += 1
    Path("Documents/seamansguide.com/webapps/_content.csv").write_text(csv)


def execute_command(args):
    if not args:
        return (f'NO COMMAND GIVEN: {args}')
    elif args[0] == 'save':
        save_json_data('config/data.json')
    elif args[0] == 'load':
        load_json_data('config/data.json')
    elif args[0] == 'web':
        url = args[1] if args[1:] else None
        web_browser(url)
    else:
        return (f'NO COMMAND FOUND: {args}')


def web_browser(url=None):
    if not url:
        url = 'http://localhost:8000/writer/author/'
    print(url)
    browser = webbrowser.get('firefox')
    browser.open(url)
