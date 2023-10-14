from pathlib import Path
from course.team import setup_team_pages
from probe.data import load_json_data, save_json_data

from probe.probe_pub import test_pub_json
from publish.publication import build_pubs
from publish.text import text_join, text_lines
from task.task import fix_tasks, task_command
from task.todo import edit_todo_list
from writer.outline import create_outlines
from writer.pub_script import pub_path, pub_script
from writer.words import measure_pub_words

from .models import Probe, TestResult
from .probe_pub import test_show_pubs


def quick_test():
    # print("No quick test defined")
    # course()
    pub()
    # tasks()
    # tests()
    # writer()
    return 'OK'


def course():
    # Student.objects.all().delete()
    # s = workspace_path(course='bacs350', project='_students.csv')
    # import_students(s)
    # print('students: ', len(Student.objects.all()))

    # Team.objects.all().delete()
    # initialize_course_data(delete=False, verbose=True, sales=True)
    # setup_teams()
    setup_team_pages()


def pub():
    # Build Pubs
    build_pubs(verbose=False, delete=False)
    text = measure_pub_words()
    print(len(text_lines(text)), 'Lines of text in word files')


def writer():
    create_outlines(pub_path('spirituality', 'Transformation'))

    # print(f'Words {pub.name}: {pub.words}')

    # pub = get_pub(x)
    # # pub.delete()
    # # create_pub(x, f'Documents/Shrinking-World-Pubs/{x}/Pub', False)
    # # create_pub_index(pub, get_pub_contents(pub))
    # print(show_pubs())
    # print(show_pub_details(pub))

    # Create Cover Images
    # path = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/poem/Images/Cover.png'
    # scale_image(path, 1600, 2560)
    # create_cover_images(path)


def tests():
    # pub = get_pub('marks')
    # print(show_pub_details(pub))
    # print(get_pub_info(pub.name))

    # test_website_pages()

    print(f'{len(Probe.objects.all())} Tests available')
    print(f'{len(TestResult.objects.all())} Test Results available')
    test_pub_json()
    test_show_pubs()


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
        save_json_data('config/publish.json', 'publish')
        save_json_data('config/course.json', 'course')
    elif args[0] == 'load':
        load_json_data('config/data.json')
        load_json_data('config/publish.json')
        load_json_data('config/course.json')
    else:
        return (f'NO COMMAND FOUND: {args}')

    # elif args[0] == 'deploy':
    #     push_JSON_data()
    #     return deploy_to_production('production')
    # elif args[0] == 'staging':
    #     push_JSON_data()
    #     return deploy_to_production('staging')
    # elif args[0] == 'export':
    #     return export_data()
    # elif args[0] == 'import':
    #     return import_data()
    # elif args[0] == 'quick':
    #     return quick_test(args)
    # elif args[0] == 'show':
    #     return show_command()
    # elif args[0] == 'users':
    #     return create_test_users()
