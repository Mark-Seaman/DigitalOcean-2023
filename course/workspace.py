from os import getenv
from pathlib import Path


def workspace_path(**kwargs):
    course = kwargs.get('course')
    student = kwargs.get('student')
    project = kwargs.get('project')
    doc = kwargs.get('doc')

    path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')

    if doc and project and course:
        path = path/course/project/doc
    elif project and course:
        path = path/course/project
    elif course:
        path = path/course
    else:
        path = path
    return path


def workspace_data(**kwargs):
    kwargs['title'] = 'STUDENT PROJECT WORKSPACE'
    return kwargs
