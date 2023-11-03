from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, TemplateView
from django.views.generic.edit import FormView

from .ai import pub_ai
from .models import Author
from .pub_script import create_pub_content, doc_view_data, pub_edit
from .publisher import pub_publish


class DocumentView(TemplateView):
    template_name = "pub_script/document.html"

    def get_context_data(self, **kwargs):
        kwargs.update(doc_view_data(**kwargs))
        return kwargs


class CreateContentForm(forms.Form):
    content = forms.CharField(label='Content Path', max_length=100)


class DocumentAddView(FormView):
    # class DocumentView(FormView):
    template_name = 'pub_script/chapter_add.html'
    form_class = CreateContentForm
    success_url = '/writer'
    # def get_success_url(self):
    #     return self.request.path[3:]

    def get_initial(self):
        initial = super().get_initial()
        initial['content'] = self.request.path[8:-4]
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(doc_view_data(**kwargs))
        return context

    def form_valid(self, form):
        path = form.cleaned_data['content']
        url = create_pub_content(path)
        return redirect(url)
        # try:
        #     url = create_pub_content(path)
        #     message = f"Pub '{path}' created successfully!"
        # except OSError as e:
        #     message = f"Failed to create directory: {str(e)}"
        # form.add_error(None, message)
        # return self.render_to_response(self.get_context_data(form=form))


class DocumentEditView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_edit(**kwargs)


class DocumentPublishView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_publish(**kwargs)


class ApplyAiView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_ai(**kwargs)


class AuthorListView(ListView):
    model = Author
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__.lower()
        context['add'] = ('/writer/author/add', 'Add Author')
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        x = self.get_object()
        model_name = x._meta.model_name
        data = {
            'title': f'{model_name} details',
            'edit': (f'{x.pk}/', f'Edit {model_name}'),
            'list': ('./', f'List of {model_name}'),
        }
        kwargs.update(data)
        return kwargs


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    template_name = 'edit.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__.lower()
        return context


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    template_name = 'edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('author_detail', kwargs={'pk': self.object.pk})


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'delete.html'
    success_url = reverse_lazy('author_list')


# FILEPATH: /path/to/your/tests.py
