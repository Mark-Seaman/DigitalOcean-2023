from pathlib import Path

from publish.document import document_title
from publish.files import read_csv_file
from publish.text import text_join
from course.course import bacs350_options, create_course, cs350_options
from course.models import Content, Course

from csv import reader


def import_course(course, delete, verbose):
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
            x.folder = Content.objects.get(course=course, doctype="week", order=week)
        elif doctype == "week":
            x.path = None
            x.title = f"Week {week}"
        x.save()
        # print(x)
        return x

    if delete:
        if verbose:
            print('DELETE', course.name)   
        delete_content(course)
    content = read_csv_file(course_content_file(course))
    for row in content:
        create_content(course, row)
        if verbose:
            print('CREATE CONTENT:', course, row)
    if verbose:
        print(f'{len(Content.objects.filter(course=course))} content objects created for {course.name}')

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


def import_all_courses(**kwargs):
    delete = kwargs.get('delete', False)
    verbose = kwargs.get('verbose', False)
    course =  kwargs.get('course')
    courses = [course] if course else ['cs350', 'bacs350']
    for c in courses :
        options = {'cs350': cs350_options, 'bacs350': bacs350_options}
        if verbose:
            print(options[c]())
        course = create_course(**(options[c]()))
        import_course(course, delete, verbose)

