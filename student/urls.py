
from django.urls import include, path

from .views_student import StudentDeleteView, StudentDetailView, StudentListView, StudentAddView, StudentUpdateView, UserUpdateView


urlpatterns = [
    # Accounts
    path('accounts/<int:pk>/',  UserUpdateView.as_view(),    name='user_edit'),
    path('accounts/',           include('django.contrib.auth.urls')),

    # Student
    path('course/<str:course>/student/',                StudentListView.as_view(),    name='student_list'),
    path('course/<str:course>/student/add',             StudentAddView.as_view(),     name='student_add'),
    path('course/<str:course>/student/<int:pk>',        StudentDetailView.as_view(),  name='student_detail'),
    path('course/<str:course>/student/<int:pk>/',       StudentUpdateView.as_view(),  name='student_edit'),
    path('course/<str:course>/student/<int:pk>/delete', StudentDeleteView.as_view(),  name='student_delete'),

]
