from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from markdown import markdown

from .models import Note
from .note import notes
from .publication import select_blog_doc, is_local


class NoteListView(ListView):
    model = Note
    template_name = 'note/note_list.html'
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        pub = kwargs.get("pub", "stacie")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(pub, doc)
        return kwargs


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note/note_detail.html'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['text'] = markdown(kwargs.get("note").text)
        pub = kwargs.get("pub", "stacie")
        doc = kwargs.get("doc", "Index.md")
        kwargs.update(select_blog_doc(pub, doc))
        return kwargs


class NoteCreateView(CreateView):
    model = Note
    template_name = 'note/note_form.html'
    fields = ['title', 'text', 'author']
    success_url = '/stacie/ThankYou.md'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        pub = kwargs.get("pub", "stacie")
        doc = kwargs.get("doc", "Index.md")
        kwargs.update(select_blog_doc(pub, doc))
        return kwargs


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'note/note_form.html'
    fields = ['title', 'text', 'author']
    success_url = '/stacie/Memories.md'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        pub = kwargs.get("pub", "stacie")
        doc = kwargs.get("doc", "Index.md")
        kwargs.update(select_blog_doc(pub, doc))
        return kwargs


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note/note_delete.html'
    success_url = '/stacie/Memories.md'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        pub = kwargs.get("pub", "stacie")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(pub, doc)
        return kwargs

# class NoteRedirectView(RedirectView):
#     permanent = False
#     query_string = True
#     pattern_name = 'note_list'

#     def get_redirect_url(self, *args, **kwargs):
#         return super().get_redirect_url(*args, **kwargs)


class StacieView(TemplateView):
    model = Note
    template_name = 'stacie.html'
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        # kwargs = super().get_context_data(**kwargs)
        pub = kwargs.get("pub", "stacie")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(pub, doc)
        kwargs = self.add_notes(
            not self.request.user.is_anonymous, doc, **kwargs)
        kwargs = self.add_subscribe(doc, **kwargs)
        return kwargs

    def add_notes(self, moderator, doc, **kwargs):
        if doc == 'Memories.md':
            text = ''
            for note in notes():
                # if moderator or note.published:
                link = f'[{note.title}](/note/{note.pk})'
                text += f'* {link}  by **{note.author}**\n'
            kwargs['notes'] = markdown(text)
            kwargs['message'] = True
        return kwargs

    def add_subscribe(self, doc, **kwargs):
        if doc == 'News.md':
            kwargs['subscribe'] = True
        return kwargs
