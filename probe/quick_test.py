from pathlib import Path

from publish.import_export import create_pub
from publish.models import Content, Pub
from publish.publication import all_pubs, build_pubs, get_pub, get_pub_info
from publish.seamanslog import random_post
from task.models import Activity, Task, TaskType
from task.task import task_command
from task.todo import edit_todo_list
from writer.writer_script import pub_script

from .models import Probe, TestResult
from .probe_images import test_image_pages


def quick_test():
    # print("No quick test defined")
    pubs()
    # test_website_pages()


def show_pubs():
    for t in ['book', 'blog', 'course', 'private']:
        print(f'\nPubs - {t}')
        for p in all_pubs(t):
            print('    ', get_pub(p.name))


def pubs():
    # Run pub scripts:
    # print(pub_script_command('project quest'.split(' ')))
    # print(pub_script(['project', 'quest']))
    # print('project quest'.split(' '))

    # Do complete rebuild
    build_pubs(False, True)
    show_pubs()


def tests():
    print(f'{len(Probe.objects.all())} Tests available'  )
    print(f'{len(TestResult.objects.all())} Test Results available'  )


def tasks():
    task_command(['week'])


def write():
    print(random_post("journey"))


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

