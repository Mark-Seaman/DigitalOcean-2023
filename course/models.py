from django.db import models
from django.urls.base import reverse_lazy
from django.contrib.auth.models import User


# --------------------
# Course
#
# name - identity of course
# title - short description
# description - summary of course content
# doc_path - lookup for lesson and project documents
# num_projects - weekly projects
# num_lessons - total number of lessons
# github_repo - directory of Github repo to pull


class Course(models.Model):
    name = models.CharField(max_length=20, default="XXX")
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(default="No Description is Set")
    doc_path = models.CharField(max_length=200, default="Documents")
    num_projects = models.IntegerField(default=14)
    num_lessons = models.IntegerField(default=42)
    github_repo = models.CharField(
        max_length=200, default="~/Github/UNC-BACS200-2022-Spring"
    )
    week = models.IntegerField(default=7)

    @property
    def image_path(self):
        return f"/static/images/shrinking-world.com/{self.name}"

    @property
    def weeks(self):
        return [
            a[0] for a in self.lessons.order_by("week").values_list("week").distinct()
        ]

    def __str__(self):
        return f"{self.pk} - {self.name} - {self.title}"

    def get_absolute_url(self):
        return reverse_lazy("course_index", args=[self.name])


# --------------------
# Content
#
# course - points to course object
# order - lesson number order
# title - title text of chapter
# week - week of class
# document - path to markdown file
# url - page to load


class Content(models.Model):
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, editable=False)
    order = models.IntegerField()
    title = models.CharField(max_length=200, default="No title")
    doctype = models.CharField(max_length=200)
    path = models.CharField(max_length=200, null=True)
    folder = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, editable=False
    )

    @property
    def document(self):
        return f"Documents/shrinking-world.com/{self.course.name}/{self.doctype}/{int(self.order):02}.md"

    @property
    def url(self):
        return f"/course/{self.course.name}/{self.doctype}/{self.order}"

    def __str__(self):
        if self.folder:
            return f"{self.course.name} week {self.folder.order} - {self.doctype} {self.order} - {self.title}"
        else:
            return f"{self.course.name} -- {self.doctype} {self.order} - {self.title}"

# --------------------
# Student


class Student(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, editable=False)
    github = models.URLField(null=True, blank=True)
    server = models.URLField(null=True, blank=True)

    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"
