from django.views.generic import RedirectView, TemplateView

from publish.files import read_json

from .ai import pub_ai
from .pub_dev import edit_doc_script, edit_files, pub_edit, pub_path, doc_view_data, pub_script, pub_url


class DocumentView(TemplateView):
    template_name = "pub_script/document.html"

    def get_context_data(self, **kwargs):
        kwargs.update(doc_view_data(**kwargs))
        return kwargs

class ProjectAddView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pub_script(['project','NEW'])
        pub_script(['chapter','NEW','NEW'])
        pub_script(['doc','NEW','NEW', 'NEW.md'])
        edit_doc_script(['NEW','NEW', 'NEW.md'])
        return pub_url('NEW','NEW', 'NEW.md')
    

class DocumentEditView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_edit(**kwargs)


class ApplyAiView(RedirectView):

    def get_redirect_url(self, **kwargs):
        return pub_ai(**kwargs)
