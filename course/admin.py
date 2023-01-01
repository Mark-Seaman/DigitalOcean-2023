from django.contrib import admin
from .models import Author, Course

admin.site.register(Course)
admin.site.register(Author)
