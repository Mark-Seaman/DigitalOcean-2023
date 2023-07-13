from django import forms
from django.shortcuts import redirect
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from .ai import pub_ai
from .pub_script import (chapter_script, create_pub_content, doc_script, doc_view_data, edit_doc_script, project_script, pub_edit, pub_publish, pub_script,
                         pub_url)


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
