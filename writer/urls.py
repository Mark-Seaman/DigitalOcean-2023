from django.urls import path

from writer.views import ApplyAiView, DocumentEditView, DocumentView, ProjectAddView

urlpatterns = [

    # Pub Script
    path('project/add', ProjectAddView.as_view()),

    # Pub Writer Views
    path("", DocumentView.as_view()),
    path("<str:pub>", DocumentView.as_view()),
    path("<str:pub>/<str:chapter>", DocumentView.as_view()),
    path("<str:pub>/<str:chapter>/<str:doc>", DocumentView.as_view()),
    path('<str:pub>/<str:chapter>/<str:doc>/', DocumentEditView.as_view()),
    path('<str:pub>/<str:chapter>/<str:doc>/ai', ApplyAiView.as_view()),
]
