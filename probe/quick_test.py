import calendar
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, localdate
from pathlib import Path
from re import sub

from course.course import get_course, weekly_content
from publish.models import Content, Pub
from publish.pub import (
    build_pubs,
    delete_pubs,
    get_pub,
    get_pub_contents,
    import_pubs,
    show_pub_content,
    show_pub_index,
    show_pub_summaries,
    show_pub_contents,
    show_pub_json,
    show_pub_words,
)
from publish.seamanslog import random_post
from publish.toc import (
    content_file,
    read_content_csv,
    table_of_contents,
    write_content_csv,
)

import toot


def quick_test():
    # print("No quick test defined")
    pubs()
    # todo()


def todo():
    print("TODO")
    # edit_todo_list()
    # edit_review_file()
    # edit_toot_file()
    # edit_blog_files()
    print(random_post("journey"))
    # article = random_article()
    # print(extract_message(article["doc"], article["url"]))


def pubs():
    print("Build Pubs")

    delete_pubs()
    build_pubs()

    # pub = get_pub("spiritual")
    # print(show_pub_summaries())
    # # show_pub_index(pub)
    # print(show_pub_words(pub))

    # print(create_pub_index(pub))

    # list_pubs()
    # show_pubs()
    # show_pub_json()

    # pub = get_pub("sampler")
    # contents = get_pub_contents(pub)
    # print(table_of_contents(pub, contents))


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
    weeks = accordion_data()
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
