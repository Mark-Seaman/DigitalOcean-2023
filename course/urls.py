from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import CourseContentView, CourseListView, ImportDataView, SlidesView, StudentListView, StudentProfileView, TeamView, home_view, login_email_view, login_username_view

urlpatterns = [

    # Student
    path('login/', login_email_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login_username/', login_username_view),

    path('course/<str:course>/home',
         CourseContentView.as_view(),  name='student_view'),

    #     # Course
    #     path('workspace', WorkspaceView.as_view()),
    #     path('workspace/<str:course>', WorkspaceView.as_view()),
    #     path('workspace/<str:course>/<int:project>', WorkspaceView.as_view()),
    #     path('workspace/<str:course>/<int:project>/<str:doc>',
    #          WorkspaceView.as_view(), name='workspace'),

    path('student/<int:pk>', StudentProfileView.as_view()),
    #     path('students', StudentListView.as_view()),
    path('import', ImportDataView.as_view()),

    # Software Engineering
    path('course/cs350', TeamView.as_view()),
    path('course/cs350/<int:team>', TeamView.as_view()),
    path('course/cs350/<int:team>/<int:milestone>', TeamView.as_view()),
    path('course/cs350/<int:team>/<int:milestone>/<int:role>', TeamView.as_view()),

    # Lessons and Projects
    path('course', CourseListView.as_view(), name='course_list'),
    path('course/<str:course>', CourseContentView.as_view(), name='course_index'),
    path('course/<str:course>/slides/<int:order>',
         SlidesView.as_view(), name='slides'),
    path('course/<str:course>/students', StudentListView.as_view()),
    path('course/<str:course>/<str:doctype>/<int:order>',
         CourseContentView.as_view()),
    path('course/<str:course>/<str:doctype>/<str:doc>',
         CourseContentView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
