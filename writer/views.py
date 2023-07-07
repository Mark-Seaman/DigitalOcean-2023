from django import forms
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from .ai import pub_ai
from .pub_script import (doc_view_data, edit_doc_script, pub_edit, pub_script,
                         pub_url)


class DocumentView(TemplateView):
    template_name = "pub_script/document.html"

    def get_context_data(self, **kwargs):
        kwargs.update(doc_view_data(**kwargs))
        return kwargs


class ProjectAddView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pub_script(['project', 'NEW'])
        pub_script(['chapter', 'NEW', 'NEW'])
        pub_script(['doc', 'NEW', 'NEW', 'NEW.md'])
        edit_doc_script(['NEW', 'NEW', 'NEW.md'])
        return pub_url('NEW', 'NEW', 'NEW.md')


class CreateChapterForm(forms.Form):
    chapter = forms.CharField(label='Chapter Name', max_length=100)


class ChapterAddView(FormView):
    template_name = 'pub_script/chapter_add.html'
    form_class = CreateChapterForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        kwargs.update(doc_view_data(**kwargs))
        kwargs['message'] = 'MY MESSAGE'
        return kwargs

    def form_valid(self, form):
        directory_path = form.cleaned_data['chapter']
        try:
            # os.makedirs(directory_path)
            print("Chapter:", directory_path)
            message = f"Directory '{directory_path}' created successfully!"
        except OSError as e:
            message = f"Failed to create directory: {str(e)}"

        # form.cleaned_data['message'] = message
        form.add_error(None, message)
        return self.render_to_response(self.get_context_data(form=form))


class DocumentEditView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_edit(**kwargs)


class ApplyAiView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_ai(**kwargs)
