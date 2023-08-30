from typing import Any, Optional
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, RedirectView, TemplateView
from django.views.generic.edit import UpdateView
from pathlib import Path
from course.import_export import import_all_courses
from course.student import import_students, student_list_data, students
from course.workspace import workspace_data, workspace_path

from publish.files import read_json
from .course import create_courses, get_course_content, initialize_course_data
from .models import Course, Student
from .slides import slides_view_context


class CourseContentView(TemplateView):
    template_name = 'course_content.html'

    def get_context_data(self, **kwargs):
        kwargs = get_course_content(self.request.user, **kwargs)
        return kwargs


class WorkspaceView(TemplateView):
    template_name = 'workspace.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['user'] = self.request.user
        kwargs.update(workspace_data(**kwargs))
        return kwargs


class ImportDataView(RedirectView):
    def get_redirect_url(self, **kwargs):
        initialize_course_data(delete=False, verbose=False, sales=False)

        # create_courses()
        # s = workspace_path(course='bacs350', project='_students.csv')
        # import_students(s)
        # import_all_courses()
        # students(verbose=True)

        return '/course/cs350'


class StudentListView(TemplateView):
    template_name = 'students.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(student_list_data())
        return kwargs


class StudentProfileView(UpdateView):
    template_name = 'edit.html'
    model = Student
    fields = ['name', 'email', 'github', 'server']

    def get_success_url(self):
        return f'/course/{self.object.course.name}'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(read_json(Path('Documents') / 'course' / 'course.json'))
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.object.user.email
        initial['name'] = f'{self.object.user.first_name} {self.object.user.last_name}'
        return initial

    def form_valid(self, form):
        student = form.save(commit=False)
        student.user.email = form.cleaned_data['email']
        name = form.cleaned_data['name'].split(' ')[:2]
        student.user.first_name, student.user.last_name = name
        student.user.save()
        return super().form_valid(form)


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


def login_email_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = get_user_model().objects.filter(email=email).first()
        if user and user.check_password(password):
            login(request, user)
            if Student.objects.filter(email=email, course__name='cs350'):
                return redirect('/course/cs350')
            elif Student.objects.filter(email=email, course__name='bacs350'):
                return redirect('/course/bacs350')
            else:
                return redirect('/course')

        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login_email.html', {'error_message': error_message})
    return render(request, 'login_email.html')


def login_username_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/course')
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login_username.html', {'error_message': error_message})
    return render(request, 'login_username.html')


@login_required
def home_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'course_home.html', context)
