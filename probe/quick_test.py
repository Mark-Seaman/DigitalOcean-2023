from pathlib import Path

from publish.models import Content, Pub
from publish.publication import get_pub_info, rebuild_pubs
from publish.seamanslog import random_post
from publish.text import line_count, text_join
from task.models import Activity, Task, TaskType
from task.task import task_command
from task.todo import edit_todo_list

from .models import Probe, TestResult


def quick_test():
    # print("No quick test defined")
    pubs()


def pubs():
    rebuild_pubs()


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


def courses():

    print("Build Courses")
    # weeks = weekly_content(get_course("bacs350"))
    # weeks = accordion_data()
    # for w in weeks:
    #     print(w)
    # create_course(**bacs350_options())
    # prepare_lesson(10)
    # prepare_lesson(11)
    # import_all_courses()

    # name = "write"
    # create_blog(name)

    # build_blogs()

    # b = Pub.objects.all().values()[0]
    # print(b)
    # f = f"blog.json"
    # print(f)
    # write_json(f, b)
    # book = get_book("journey")
    # for part in list_parts(book):
    #     print(part)
    #     for c in part["chapters"]:
    #         print(c)

    # print(test_book_import())

    print("Show course content")
    course = get_course("bacs350")
    print(show_content(course))
    # print(test_export_courses())
