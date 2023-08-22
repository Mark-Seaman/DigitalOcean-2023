from csv import DictReader
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from publish.files import write_csv_file

from .import_export import import_records
from .models import Course, Student


def table_data(title, rows, columns):
    return dict(title=title, rows=rows, columns=columns)


def button_html(url, text):
    return f'<a class="btn" href="{url}">{text}</a>'


def link_html(url, text):
    return f'<a class="text-success" href="{url}">{text}</a>'


def make_user(**kwargs):
    name = kwargs.get('name')
    first, last = name.split(' ')[:2]
    username = f'{first}{last}'.replace(' ', '')
    email = kwargs.get('email', f'{username}@shrinking-world.com')
    kwargs = dict(username=username, first_name=first,
                  last_name=last, email=email)
    user, _ = get_user_model().objects.get_or_create(
        username=username, defaults=kwargs)
    user.username = username
    user.first_name = first
    user.last_name = last
    user.save()
    return user


def create_student(**kwargs):
    user = make_user(**kwargs)
    course_name = kwargs.get('course')
    if course_name:
        course = Course.objects.get(name=course_name)
        student, _ = Student.objects.get_or_create(user=user, course=course)
        return student


def list_students():
    def record(x):
        url1 = f'/student/{x.pk}/'
        label1 = f'{x.name} Profile'
        return dict(name=x.name,
                    email=x.user.email,
                    url1=button_html(url1, label1))

    objects = Student.objects.all().order_by('user__last_name')
    objects = [record(x) for x in objects]
    return objects


def student_list_data():
    title = f'UNC Students'
    tables = []
    fields = ['Student name', 'Email', 'Course']
    tables.append(table_data(title, list_students(), fields))
    data = {
        'tables': tables,
        'add_button': button_html("/student/add", 'Add New Student'),
    }
    return data


def student_detail(student):
    return model_to_dict(student, fields=('name', 'email', 'course'))


def students(**kwargs):
    return Student.objects.filter(**kwargs).order_by('user__last_name')


def export_students(path=None):
    def row(s):
        return [s.user.first_name, s.user.last_name, s.email, s.whatsapp, s.country, s.program]

    header = ['first_name', 'last_name', 'email',
              'whatsapp', 'country', 'program']
    table = [header] + [row(s) for s in students()]
    write_csv_file(path, table)
    return f"{len(Student.objects.all())} Student objects exported to {path}\n"


def import_students(path):
    # return import_records(path, create_student)
    with open(path) as file:
        reader = DictReader(file)
        for row in reader:
            name = row.get('user')
            email = row.get('user_email')
            course = 'cs350' if row.get(
                'product_name') == 'Software Engineering' else 'bacs350'
            create_student(name=name, email=email, course=course)
