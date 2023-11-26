from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, TemplateView

from .models import Note


class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
