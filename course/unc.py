from pathlib import Path

from .course import course_settings
from .models import Course
from publish.days import days_ago, to_date
from publish.files import read_csv_file, write_csv_file
from publish.text import text_join


def course_schedules():
    return text_join([schedule_csv(course) for course in Course.objects.all()])


# UNC Schedule Spring 2022 for MWF classes
def create_unc_schedule_MWF():
    output = []
    d = to_date('2022-08-22')
    lesson = 1
    for w in range(15):
        output.append([days_ago(d, -w * 7), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 7 - 2), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 7 - 4), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 7 - 4), w + 1, '', w + 1])
    return output


# UNC Schedule Fall 2022 for MW classes
def create_unc_schedule_MW():

    output = []
    d = to_date('2022-08-22')
    lesson = 1
    for w in range(15):
        output.append([days_ago(d, -w * 7), w+1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 7 - 2),  w+1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 7 - 2),  w+1, '', w + 1])
    return output


# UNC Schedule Spring 2022 for T Th classes
def create_unc_schedule_TTh():
    output = []
    lesson = 1
    d = to_date('2022-08-23')
    for w in range(7):
        output.append([days_ago(d, -w * 14), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 14 - 2), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 14 - 7), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 14 - 9), w + 1, lesson, ''])
        lesson += 1
        output.append([days_ago(d, -w * 14 - 9), w + 1, '', w + 1])
    return output


def schedule_csv(course):
    def content(row):
        d = row[0]
        w = row[1]
        l = f' - Lesson {row[2]}' if row[2] else ''
        p = f' - Project {row[3]}' if row[3] else ''
        return f'{d} - Week {w}{l}{p}'

    schedule = Path(course.doc_path) / 'schedule.csv'
    table = read_csv_file(schedule)
    return f'\n\nSchedule for {course.name}\n\n' + text_join([content(row) for row in table])


def schedule_view_data(course):

    def lessons(week):
        return [(d[0], d[2]) for d in schedule if d[1] == str(week) and d[2]]

    def project(week):
        for d in schedule:
            if d[1] == str(week) and d[3]:
                return d[0], d[3]

    def plan(week):
        return dict(week=week, lessons=lessons(week), project=project(week))

    def print_lesson_plan(week_data):
        for w in week_data:
            print(f'{settings["week_label"]} #{w["week"]}')
            for x in w["lessons"]:
                print(f'    {x[0]} - Lesson {x[1]}')
            print(f'    {w["project"][0]} - Project {w["project"][1]}')

    schedule = read_csv_file(Path(course.doc_path) / 'schedule.csv')
    settings = course_settings(**dict(course=course.name))
    n = settings['num_weeks']
    # p = settings['periods_per_week']
    weeks = [plan(n+1) for n in range(n)]
    print_lesson_plan(weeks)

    return weeks


def write_schedule_csv(course_name, schedule):
    course = Course.objects.get(name=course_name)
    schedule_path = Path(course.doc_path) / 'schedule.csv'
    write_csv_file(schedule_path, schedule)


def view_class_content():
    courses = ['bacs200', 'bacs350', 'cs350']
    for c in courses:
        course = Course.objects.get(name=c)
        print(schedule_view_data(course))
