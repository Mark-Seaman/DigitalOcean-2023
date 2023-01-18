import calendar
from pathlib import Path
from re import findall, sub
from django.template.loader import render_to_string

from course.course import get_course, weekly_content
from probe.probe_documents import test_documents_fix_chars
from publish.import_export import import_pub
from publish.models import Content, Pub
from publish.pub import (
    build_pubs,
    delete_pubs,
    get_pub,
    get_pub_contents,
)
from publish.seamanslog import random_post
from publish.toc import (
    content_file,
    read_content_csv,
    table_of_contents,
    write_content_csv,
)
from task.models import Activity, Task, TaskType
from task.task import task_import_files, time_percentage, time_summary, time_table, time_totals
from task.todo import edit_todo_list


def quick_test():
    # print("No quick test defined")
    # pubs()
    # todo()
    # write()
    # task()
    fix_tasks()


def task():
    task_import_files(200)

    totals = time_totals(200)
    table, total = time_percentage(totals)
    for t in table:
        a = Activity.objects.filter(name=t[0].strip())
        if a:
            print(f'{str(a[0]):15} - {t[0]} - {t[1]} hr - {t[2]}%')
        else:
            print('\n*********** No Activity', t[0].strip())
            print()


def fix_tasks():
    def find_tasks(text):
        return findall(r'\n[A-Z][a-z]* *\d*', text)

    def replace_task(t1, t2, text):
        return sub(rf'\n{t1} *(\d*)', fr'\n{t2} \1', text)

    def rename_task(old_task, new_task):
        path = Path("Documents/markseaman.info/history/2023/01/17")
        text = path.read_text()
        text = replace_task(old_task, new_task, text)
        path.write_text(text)

    rename_task('Tools', 'Code')

    # for t in Task.objects.filter(name='Career'):
    #     t.name = 'Business'
    #     t.save()

    # for t in Task.objects.filter(name='Networking'):
    #     t.name = 'Business'
    #     t.save()

    # table = time_table("week", 100)
    # print(table['table'])

    # define_activity('Teach', 'Work')
    # define_activity('Write', 'Work')
    # define_activity('Business', 'Work')
    # define_activity('Tools', 'Work')
    # define_activity('Network', 'Work')
    # define_activity('Grow', 'Grow')
    # define_activity('Church', 'People')
    # define_activity('People', 'People')
    # define_activity('Fun', 'Fun')

    # for a in Activity.objects.all():
    #     print(a)

    # for a in table['table']:
    #     print(a)

    # print(time_summary())


def define_activity(name, type):
    type = TaskType.objects.get_or_create(name=type)[0]
    return Activity.objects.get_or_create(name=name, type=type)[0]


def write():
    # edit_review_file()
    # edit_toot_file()
    # edit_blog_files()
    print(random_post("journey"))
    # article = random_article()
    # print(extract_message(article["doc"], article["url"]))


def todo():
    print("TODO")
    edit_todo_list()


def pubs():
    print("Build Pubs")
    # delete_pubs()
    build_pubs()
    # import_pub_content()


def import_pub_content():
    pub = get_pub("quest")
    import_pub(pub)

    contents = get_pub_contents(pub)
    print(table_of_contents(pub, contents, False))

    # print(show_pub_summaries())
    # # show_pub_index(pub)
    # print(show_pub_words(pub))

    # print(create_pub_index(pub))
    # print(test_documents_fix_chars())

    # list_pubs()
    # show_pubs()
    # show_pub_json()

    # pub = get_pub("sampler")


def create_sampler_index():
    def create_content_file(pub):
        content = content_file(pub)
        if not content.exists():
            write_content_csv(pub)

    pub = get_pub("sampler")
    create_content_file(pub)
    print(read_content_csv(pub))

    contents = get_pub_contents(pub)


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
    weeks = weekly_content(get_course("bacs350"))
    # weeks = accordion_data()
    for w in weeks:
        print(w)
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

    # print("Show course content")
    # print(test_export_courses())
