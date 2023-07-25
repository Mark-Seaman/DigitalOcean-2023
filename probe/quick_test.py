from pathlib import Path
from re import DOTALL, findall

from probe.probe_pub import test_pub_json
from publish.import_export import create_pub
from publish.publication import (build_pubs, get_pub, get_pub_contents,
                                 show_pubs)
from publish.text import text_join, text_lines
from publish.toc import create_pub_index
from task.task import task_command
from task.todo import edit_todo_list
from writer.outline import create_outlines
from writer.pub_script import pub_path, pub_script

from .models import Probe, TestResult
from .probe_pub import test_show_pubs


def quick_test():
    # print("No quick test defined")
    pubs()

    # Run Tests
    # tests()
    # writer()

    return 'OK'

def writer():
    # path = pub_path('spirituality','Transformation','Outline.md')
    # test_extraction(path)
    # create_index(path)
    # create_outlines_ai(path)
    # outline = path.read_text()
    # fragments = split_outline(outline)
    # print(fragments)

    create_outlines(pub_path('spirituality','Transformation'))


def pubs():

    # Run pub scripts:
    # print(pub_list())

    # Create Cover Images
    # path = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/poem/Images/Cover.png'
    # scale_image(path, 1600, 2560)
    # create_cover_images(path)

    # Build Pubs
    # create_pub('spirituality', 'Documents/Shrinking-World-Pubs/spirituality/Pub', True)
    # pub = get_pub('spirituality')
    # create_pub_index(pub, get_pub_contents(pub)) 
    # build_pubs(verbose=True, delete=True)
    print(show_pubs())



def tests():
    # pub = get_pub('marks')
    # print(show_pub_details(pub))
    # print(get_pub_info(pub.name))

    # test_website_pages()

    print(f'{len(Probe.objects.all())} Tests available'  )
    print(f'{len(TestResult.objects.all())} Test Results available'  )
    test_pub_json()
    test_show_pubs()

def tasks():
    task_command(['week'])


def execute_pub_script(text):
    return text_join([pub_script(line.strip().split(' ')) for line in text_lines(text) if line.strip()])


# def writer():
#     command = '''
#         project ai
#         chapter ai Tips
#         chapter ai Mistakes
#         chapter ai AIPlaybook
#         chapter ai GettingStarted
#         chapter ai WriteWithAI
#         doc ai Tips Blog.md
#       '''
#     print(execute_pub_script(command))


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

