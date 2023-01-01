from django.contrib.auth.models import User
from django.db import models

from course.models import Course


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, editable=False, null=True)
    github = models.URLField(default="https://github.com")
    server = models.URLField(default="https://digitalocean.com")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return '/course/bacs350'

    @property
    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @staticmethod
    def get_me(user):
        s = Student.objects.get_or_create(user=user)[0]
        s.course = Course.objects.get(pk=1)
        s.save()
        return s
