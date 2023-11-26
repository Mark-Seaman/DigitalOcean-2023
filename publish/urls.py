from django.urls import path

from publish.views_note import NoteListView

from .views import BouncerRedirectView, ContactView, PubDetailView, PubLibraryView, PubListView, PubRedirectView, PubView

urlpatterns = [

    path('favicon.ico', PubLibraryView.as_view()),

    # Pub Redirect
    path("", PubRedirectView.as_view()),
    path("pubs", PubLibraryView.as_view(), name="pub_list"),
    path("pubs/<str:pub_type>", PubListView.as_view(), name="pub_list"),
    path("<int:id>", BouncerRedirectView.as_view()),

    # Display a pub document
    path("<str:pub>", PubDetailView.as_view(), name="pub_detail"),
    path("<str:pub>/contact", ContactView.as_view()),
    path("<str:pub>/<str:doc>", PubView.as_view(), name="pub"),

    # Notes
    path('note/', NoteListView.as_view(), name='note_list'),
]
