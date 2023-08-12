from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=20, default="XXX")
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, editable=False, null=True)
    github = models.URLField(default="https://github.com")
    server = models.URLField(default="https://digitalocean.com")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
