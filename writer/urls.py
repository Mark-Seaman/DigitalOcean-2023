from django.urls import path

from writer.views import (ApplyAiView, AuthorCreateView, AuthorDeleteView, AuthorDetailView, AuthorListView, AuthorUpdateView, DocumentAddView,
                          DocumentEditView, DocumentView, DocumentPublishView)

urlpatterns = [
    # Author views
    path('author/', AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author_detail'),
    path('author/add', AuthorCreateView.as_view(), name='author_add'),
    path('author/<int:pk>/', AuthorUpdateView.as_view(), name='author_edit'),
    path('author/<int:pk>/delete',
         AuthorDeleteView.as_view(), name='author_delete'),

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
    path('<str:pub>/<str:chapter>/<str:doc>/publish',
         DocumentPublishView.as_view()),
    path('<str:pub>/<str:chapter>/<str:doc>/ai', ApplyAiView.as_view()),

]
