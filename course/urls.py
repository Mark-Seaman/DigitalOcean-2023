from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from student.views_student import StudentView

from .views_course import CourseContentView, CourseListView, SlidesView
from .views_game import UrlGameAnswer, UrlGameQuestion, UrlGameStart

urlpatterns = [

    path('', include('student.urls')),

    # Course
    path('course/<str:course>/home', StudentView.as_view(),  name='student_view'),
    path('course', CourseListView.as_view(), name='course_list'),

    # Lessons and Projects
    path('course/<str:course>', CourseContentView.as_view(), name='course_index'),
    path('course/<str:course>/slides/<int:order>', SlidesView.as_view(), name='slides'),
    path('course/<str:course>/<str:doctype>/<int:order>', CourseContentView.as_view()),
    # path('course/<str:course>/<str:doctype>/<str:doc>', CourseDocView.as_view()),

    # URL Game
    path('course/<str:course>/url-start', UrlGameStart.as_view()),
    path('course/<str:course>/url-question/<int:pk>', UrlGameQuestion.as_view()),
    path('course/<str:course>/url-answer/<int:pk>', UrlGameAnswer.as_view()),
    # path('course/<str:course>/url-game-done/<str:name>', UncUrlGameDone.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
