from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Note


class NoteListView(ListView):
    model = Note
    template_name = 'note/note_list.html'
    context_object_name = 'notes'


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note/note_detail.html'
    context_object_name = 'note'


class NoteCreateView(CreateView):
    model = Note
    template_name = 'note/note_form.html'
    fields = ['title', 'text', 'author']
    success_url = '/note/'


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'note/note_form.html'
    fields = ['title', 'text', 'author', 'published']
    success_url = '/note/'


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note/note_delete.html'
    success_url = '/note/'


# class NoteRedirectView(RedirectView):
#     permanent = False
#     query_string = True
#     pattern_name = 'note_list'

#     def get_redirect_url(self, *args, **kwargs):
#         return super().get_redirect_url(*args, **kwargs)
