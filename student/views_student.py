from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView

from course.course import course_settings
from .models import Student


class StudentView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return '/course/bacs350'
        student = Student.get_me(self.request.user).pk
        return f'/course/bacs350/student/{student}/'


class StudentListView(ListView):
    template_name = 'student/list.html'
    model = Student
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['site_title'] = 'Student Websites'
        return kwargs

    def get_queryset(self):
        return super().get_queryset().order_by('user__last_name')


class StudentDetailView(DetailView):
    template_name = 'student/detail.html'
    model = Student
    context_object_name = 'student'


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "student/edit.html"
    model = Student
    fields = '__all__'
    success_url = '/course/bacs350'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(course_settings(**dict(course='bacs350')))
        return kwargs



class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student/delete.html'
    success_url = '/course/bacs350'


class StudentAddView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'student/add.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(course_settings(**dict(course='bacs350')))
        # course = kwargs['course_object']
        return kwargs

    def get_absolute_url(self):
        return '/course/bacs350'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "registration/account_edit.html"
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    # success_url = reverse_lazy('student_view', args=('bacs350',))
    success_url = '/course/bacs350'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(course_settings(**dict(course='bacs350')))
        # course = kwargs['course_object']
        return kwargs


def list_user_records():
    for u in User.objects.all().order_by('pk'):
        print(u.pk, u.first_name, u.last_name, u.username, u.email)

