from pathlib import Path
from sys import version_info
from probe.probe_pub import test_pub_info
from publish.files import write_json

from publish.import_export import create_pub, pub_json_path
from publish.models import Content, Pub
from publish.publication import all_pubs, build_pubs, get_pub, get_pub_info, show_pub_details, show_pubs
from publish.seamanslog import random_post
from publish.text import text_join, text_lines
from task.models import Activity, Task, TaskType
from task.task import task_command
from task.todo import edit_todo_list
from writer.pub_dev import pub_script

from .models import Probe, TestResult
from .probe_images import test_image_pages


def quick_test():
    # print("No quick test defined")
    # pubs()
    save_model()

    return 'OK'


def pubs():
    # Run pub scripts:

    # Do complete rebuild
    build_pubs(False, True)
    print(show_pubs())


def save_model():
    def save_pub_json(name):
        model = Pub
        pub = model.objects.get(name=name)
        json_path = pub_json_path(name, pub.doc_path)
        data = {}
        for field in pub._meta.get_fields():
            if field.concrete:
                field_name = field.name
                data[field_name] = getattr(pub, field_name)
        write_json(json_path, data)

    # name='journey'
    # save_pub_json(name)
    for pub in all_pubs():
        # save_pub_json(pub.name)
        json_path = pub_json_path(pub.name, pub.doc_path)
        print(json_path.read_text())

def tests():
    # pub = get_pub('marks')
    # print(show_pub_details(pub))
    # print(get_pub_info(pub.name))

    # test_website_pages()

    print(f'{len(Probe.objects.all())} Tests available'  )
    print(f'{len(TestResult.objects.all())} Test Results available'  )


def tasks():
    task_command(['week'])


def execute_pub_script(text):
    return text_join([pub_script(line.strip().split(' ')) for line in text_lines(text) if line.strip()])


def writer():
    command = '''
        project ai
        chapter ai Tips
        chapter ai Mistakes
        chapter ai AIPlaybook
        chapter ai GettingStarted
        chapter ai WriteWithAI
        doc ai Tips Blog.md
      '''
    print(execute_pub_script(command))


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

