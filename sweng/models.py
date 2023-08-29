from django.contrib.auth.models import AbstractUser, Group, Permission
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


class SWUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    # Set a unique related_name for the groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        related_name='sw_users'  # Use a different name, e.g., 'sw_users'
    )

    # Set a unique related_name for the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        # Use a different name, e.g., 'sw_users_permissions'
        related_name='sw_users_permissions'
    )
