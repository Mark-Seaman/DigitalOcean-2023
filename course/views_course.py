from django.views.generic import ListView, TemplateView
from pathlib import Path

from publish.files import read_json
from .course import get_course_content
from .models import Course
from .slides import slides_view_context


class CourseContentView(TemplateView):
    template_name = 'course_content.html'

    def get_context_data(self, **kwargs):
        kwargs = get_course_content(self.request.user, **kwargs)
        return kwargs


class CourseListView(ListView):
    template_name = 'course_list.html'
    model = Course

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(read_json(Path('Documents') / 'course' / 'course.json'))
        return kwargs


class SlidesView(TemplateView):
    template_name = 'course_slides.html'

    def get_context_data(self, **kwargs):
        return slides_view_context(**kwargs)
