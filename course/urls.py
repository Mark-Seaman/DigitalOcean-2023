from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views_course import CourseContentView, CourseListView, SlidesView, home_view, login_email_view, login_username_view

urlpatterns = [

    # Student
    path('login/', login_email_view, name='login'),
    path('login_username/', login_username_view),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('course/<str:course>/home',
         CourseContentView.as_view(),  name='student_view'),

    # Course
    path('course', CourseListView.as_view(), name='course_list'),

    # Lessons and Projects
    path('course/<str:course>', CourseContentView.as_view(), name='course_index'),
    path('course/<str:course>/slides/<int:order>',
         SlidesView.as_view(), name='slides'),
    path('course/<str:course>/<str:doctype>/<int:order>',
         CourseContentView.as_view()),
    path('course/<str:course>/<str:doctype>/<str:doc>',
         CourseContentView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
