from django.contrib.auth.models import User

from student.models import Student
from course.models import Course


def list_users():
    for user in User.objects.all():
        print(user.pk, user.username, user.first_name, user.last_name, user.email)


def list_students():
    for s in Student.objects.all():
        s.course = Course.objects.get(pk=1)
        s.save()
        print(s.pk, s.name, s.course, s.user.pk, s.user.username, s.user.first_name, s.user.last_name, s.user.email)

# python manage.py shell
