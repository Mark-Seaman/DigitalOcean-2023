from csv import DictReader
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from course.user import make_user

from publish.files import write_csv_file

from .import_export import import_records
from .models import Course, Student


def table_data(title, rows, columns):
    return dict(title=title, rows=rows, columns=columns)


def button_html(url, text):
    return f'<a class="btn btn-success" href="{url}">{text}</a>'


def link_html(url, text, target='page'):
    return f'<a class="text-success" href="{url}" target="{target}">{text}</a>'


def create_student(**kwargs):
    user = make_user(**kwargs)
    course_name = kwargs.get('course')
    if course_name:
        course = Course.objects.get(name=course_name)
        name = f'{user.first_name} {user.last_name}'
        email = user.email
        kwargs = dict(course=course, github='https://github.com',
                      server='https://digitalocean.com')
        student, _ = Student.objects.get_or_create(
            user=user, course=course, defaults=kwargs)
        student.name = name
        student.email = email
        student.save()
        return student


def list_students(course):
    def record(x):
        try:
            if not x.name or not x.email:
                x.name = f'{x.user.first_name} {x.user.last_name}'
                x.email = x.user.email
                x.save()
            url1 = f'/student/{x.pk}'
            label1 = x.name
            url2 = x.github
            label2 = x.github
            url3 = x.server
            label3 = x.server
            return dict(url1=link_html(url1, label1, 'student'),
                        course=x.course.name,
                        email=x.user.email,
                        url2=link_html(url2, label2, 'github'),
                        url3=link_html(url3, label3, 'server'))
        except:
            print("**** EXCEPTION: x")

    objects = students()
    if course:
        objects = objects.filter(course__name=course)
    objects = [record(x) for x in objects]
    return objects


def student_list_data(course):
    title = f'UNC Students'
    tables = []
    fields = ['Student', 'Course', 'Email', 'Github', 'Server']
    tables.append(table_data(title, list_students(course), fields))
    data = {
        'tables': tables,
        'add_button': button_html("/student/add", 'Add New Student'),
    }
    return data


def student_detail(student):
    return model_to_dict(student, fields=('name', 'email', 'course'))


def students(verbose=False, **kwargs):
    all = Student.objects.filter(
        **kwargs).order_by('course__name', 'user__last_name')
    if verbose:
        for s in all:
            try:
                if not s or s is None:
                    print('NONE')
                else:
                    print(f'{s.name:30} {s.email:30} {s.course.name}')
            except:
                print('EXCEPTION')
    return all


def export_students(path=None):
    def row(s):
        return [s.name, s.user.email, s.course.name]

    header = ['name', 'email', 'course']
    table = [header] + [row(s) for s in students()]
    write_csv_file(path, table)
    return f"{len(Student.objects.all())} Student objects exported to {path}\n"


def import_students(path):
    with open(path) as file:
        reader = DictReader(file)
        for row in reader:
            name = row.get('name')
            email = row.get('email')
            course = row.get('course')
            if name != 'Stacie Seaman':
                create_student(name=name, email=email, course=course)


def import_sales(path):
    def select_course(**kwargs):
        course = row.get('product_name')
        if course == 'Software Engineering':
            course = 'cs350'
        if course == 'Python Web Apps':
            course = 'bacs350'
        return course

    with open(path) as file:
        reader = DictReader(file)
        for row in reader:
            name = row.get('user')
            email = row.get('user_email')
            create_student(name=name, email=email, course=select_course(**row))
