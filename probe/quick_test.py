from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password
from pathlib import Path

from course.import_export import import_all_courses
from course.models import Course, Student
from course.student import import_students, students
from probe.probe_pub import test_pub_json
from publish.publication import show_pubs
from publish.text import text_join, text_lines
from task.task import fix_tasks, task_command
from task.todo import edit_todo_list
from writer.outline import create_outlines
from writer.pub_script import pub_path, pub_script

from .models import Probe, TestResult
from .probe_pub import test_show_pubs


def quick_test():
    # print("No quick test defined")
    # pubs()
    # tests()
    # writer()
    # tasks()
    course()


def course():
    s = Student.objects.get(
        user__email='luna0500@bears.unco.edu', course__name='cs350')
    print('login: ', s.name, 'OK' if s.user.check_password('CS350') else 'Failed')

    # import_all_courses(verbose=False)
    # Student.objects.all().delete()
    # import_students('students2.csv')
    # for s in Student.objects.all():
    # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')
    # students(True)
    # # assert len(students(course__name='cs350')) == 13
    # # assert len(students(course__name='bacs350')) == 14

    # s = Student.objects.get(
    #     user__username='RyanLunas', course__name='cs350')
    # u = s.user
    # assert s
    # assert u

    # # u.password = make_password('CS350')
    # # u.save()

    # print(f'{s.name:30} {s.user.email:30} {s.course.name:10} {s.user.password}')

    # # make_password('CS350')
    # a = authenticate(username=u.username, password='CS350')
    # c = u.check_password('CS350')

    # print(f'{s.name} -- auth {a} -- password {c}')
    # u = get_user_model().objects.filter(email=email).first()
    #     if user and user.check_password(password)
    # user = authenticate(request, username=username, password=password)
    #     if user is not None:
    return 'OK'


def writer():
    create_outlines(pub_path('spirituality', 'Transformation'))


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

    print(f'{len(Probe.objects.all())} Tests available')
    print(f'{len(TestResult.objects.all())} Test Results available')
    test_pub_json()
    test_show_pubs()


def tasks():
    fix_tasks()
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
