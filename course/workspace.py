from os import getenv
from pathlib import Path

from publish.files import read_json
from publish.document import document_body, document_html, document_title

from .student import students


def workspace_path(**kwargs):
    course = kwargs.get('course')
    student = kwargs.get('student')
    project = kwargs.get('project')
    if project:
        project = str(project)
    doc = kwargs.get('doc')

    # path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')
    path = Path('Documents/Shrinking-World-Pubs')

    if doc and project and course:
        path = path/course/project/doc
    elif project and course:
        path = path/course/project
    elif course:
        path = path/course
    else:
        path = path
    return path


def read_workspace_doc(path):
    if path.exists():
        if path.is_dir():
            path = path/'Index.md'
        if path.is_file():
            text = path.read_text()
            markdown = document_body(text)
            html = document_html(markdown)
            title = document_title(text)
            return title, html
    return 'Document Missing', 'Could not find the workspace document'


def workspace_data(**kwargs):
    # kwargs = course_settings(**kwargs)
    course = kwargs.get('course', 'bacs350')
    json = Path("Documents") / "shrinking-world.com" / \
        course / "course.json"
    settings = read_json(json)
    kwargs.update(settings)
    user = kwargs.get('user')
    path = workspace_path(**kwargs)
    kwargs['title'], kwargs['html'] = read_workspace_doc(path)
    if not user.is_anonymous:
        kwargs['student'] = students(user=user).first()
    return kwargs
