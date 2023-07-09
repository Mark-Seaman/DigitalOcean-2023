from django.urls import path

from writer.views import (ApplyAiView, DocumentAddView,
                          DocumentEditView, DocumentView, DocumentPublishView)

urlpatterns = [

    # Pub Writer Document Add
    path("add", DocumentAddView.as_view()),
    path("<str:pub>/add", DocumentAddView.as_view()),
    path("<str:pub>/<str:chapter>/add", DocumentAddView.as_view()),

    # Pub Writer Document View
    path("", DocumentView.as_view()),
    path("<str:pub>", DocumentView.as_view()),
    path("<str:pub>/<str:chapter>", DocumentView.as_view()),
    path("<str:pub>/<str:chapter>/<str:doc>", DocumentView.as_view()),
    path('<str:pub>/<str:chapter>/<str:doc>/', DocumentEditView.as_view()),
    path('<str:pub>/<str:chapter>/<str:doc>/publish', DocumentPublishView.as_view()),
    path('<str:pub>/<str:chapter>/<str:doc>/ai', ApplyAiView.as_view()),

]
