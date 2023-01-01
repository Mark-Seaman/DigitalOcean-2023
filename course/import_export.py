from pathlib import Path

from publish.document import document_title
from publish.files import read_csv_file
from publish.text import text_join
from course.course import bacs350_options, create_course
from course.models import Content, Course

from csv import reader


def import_course(course):
    def create_content(course, row):
        # print(row)
        if row[3:]:
            docpath, doctype, week, order = row
        else:
            docpath, doctype, week = row
            order = week
        x = Content.objects.get_or_create(course=course, doctype=doctype, order=order)[
            0
        ]
        path = Path(docpath)
        if path.exists() and path.is_file():
            x.path = path
            x.title = document_title(path)
            x.folder = Content.objects.get(doctype="week", order=week)
        elif doctype == "week":
            x.path = None
            x.title = f"Week {week}"
        x.save()
        # print(x)
        return x

    delete_content(course)
    content = read_csv_file(course_content_file(course))
    for row in content:
        create_content(course, row)


def delete_content(course):
    Content.objects.filter(course=course).delete()


def export_course(course):
    save_content(course)


def save_content(course):
    text = find_content(course)
    return course_content_file(course).write_text(text)


def read_content(course):
    return course_content_file(course).read_text()


def find_content(course):
    csv = ""
    # for i in range(14):
    #     csv += f"{course.doc_path},week,{i+1}\n"
    for i in Content.objects.filter(course=course):
        if i.doctype == 'week':
            csv += f"{i.document},{i.doctype},{i.order}\n"
        else:
            csv += f"{i.document},{i.doctype},{i.folder.order},{i.order}\n"
    return csv


def course_content_file(course):
    return Path(course.doc_path) / "content.csv"


def import_all_courses():
    # Course.objects.all().delete()
    # import_course(create_course(**bacs200_options()))
    # import_course(create_course(**cs350_options()))
    c = Course.objects.filter(name="cs350")
    if c:
        c[0].delete()
    c = Course.objects.filter(name="bacs200")
    if c:
        c[0].delete()
    import_course(create_course(**bacs350_options()))
