from requests import get

from course.course import get_course, show_content
from publish.text import text_lines
from course.import_export import (
    export_course,
    import_course,
    read_content,
)


def test_import_courses():
    course = get_course("bacs350")
    import_course(course)
    return show_content(course)
    # print("This test is disabled: test_import_courses()")
    # return "This test is disabled: test_import_courses()"


def test_export_courses():
    course = get_course("bacs350")
    export_course(course)
    import_course(course)
    content = read_content(course)
    return content


def test_course_content():
    course = get_course("bacs350")
    return show_content(course)


def test_course_bacs350_project():
    html = get("http://shrinking-world.com/course/bacs350/project/1").text
    return f"http://shrinking-world.com/course/bacs350/project/1 -- {len(text_lines(html))} Lines"


def test_course_bacs350_lesson():
    html = get("http://shrinking-world.com/course/bacs350/lesson/1").text
    return f"http://shrinking-world.com/course/bacs350/lesson/1 -- {len(text_lines(html))} Lines"


def test_course_bacs350_page():
    html = get("http://shrinking-world.com/course/bacs350").text
    return f"http://shrinking-world.com/course/bacs350 -- {len(text_lines(html))} Lines"
