from django.urls import path

from .views_note import NoteCreateView, NoteDeleteView, NoteDetailView, NoteListView, NoteUpdateView, StacieView
from .views import BouncerRedirectView, ContactView, PubDetailView, PubLibraryView, PubListView, PubRedirectView, PubView

urlpatterns = [

    path('favicon.ico', PubLibraryView.as_view()),

    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("pubs", PubLibraryView.as_view(), name="pub_list"),
    path("pubs/<str:pub_type>", PubListView.as_view(), name="pub_list"),
    path("<int:id>", BouncerRedirectView.as_view()),

    # Notes
    path('note/', NoteListView.as_view(), name='note_list'),
    path('note/<int:pk>', NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/', NoteUpdateView.as_view(), name='note_edit'),
    path('note/add', NoteCreateView.as_view(), name='note_add'),
    path('note/<int:pk>/delete',  NoteDeleteView.as_view(), name='note_delete'),

    # Stacie
    path('stacie', StacieView.as_view()),
    path('stacie/<str:doc>', StacieView.as_view()),


    # Display a pub document
    path("<str:pub>", PubDetailView.as_view(), name="pub_detail"),
    path("<str:pub>/contact", ContactView.as_view()),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),


]
