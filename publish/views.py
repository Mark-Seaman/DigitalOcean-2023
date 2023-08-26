from django.views.generic import RedirectView, TemplateView

from .files import read_json
from .import_export import refresh_pub_from_git
from .models import Pub
from .publication import bouncer_redirect, is_local, pub_redirect, read_menu, select_blog_doc


class BouncerRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        x = bouncer_redirect(kwargs.get('id'))
        if x:
            return x
        host = self.request.get_host()
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", 'Index.md')
        return pub_redirect(host, pub, doc)


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        pub = 'marks'
        doc = kwargs.get("doc", "contact")
        kwargs = select_blog_doc(pub, doc)
        return kwargs


class PubRedirectView(RedirectView):
    url = '/pubs'


class PubView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        local_host = is_local(self.request.get_host())
        kwargs = select_blog_doc(pub, doc, local_host)
        return kwargs


class PubLibraryView(TemplateView):
    template_name = "pub/library.html"

    def get_context_data(self, **kwargs):
        collections = [
            get_collection('course', 'Courses'),
            get_collection('book', 'Books about Life'),
            get_collection('blog', 'Blogs'),
            get_collection('private', 'Private Blogs'),
        ]
        local_host = is_local(self.request.get_host())
        menu = read_menu("static/js/nav_blog.json", local_host)
        kwargs = dict(collections=collections, menu=menu,
                      site_title="Shrinking Word Publication Library", site_subtitle="All Publications")
        return kwargs


def get_collection(pub_type, title):
    return {'type': title, 'pubs': Pub.objects.filter(pub_type=pub_type)}


class PubListView(TemplateView):

    template_name = "pub/list.html"
    model = Pub
    context_object_name = "pubs"

    def get_context_data(self, **kwargs):
        pub_type = self.kwargs.get('pub_type')
        pubs = Pub.objects.filter(pub_type=pub_type)
        local_host = is_local(self.request.get_host())
        menu = read_menu("static/js/nav_blog.json", local_host)
        kwargs = dict(pubs=pubs, menu=menu, site_title="Shrinking Word Publication Library",
                      site_subtitle="A Seaman's Guides")
        return kwargs


class PubDetailView(TemplateView):
    template_name = "pub_script/cover.html"

    def get_context_data(self, **kwargs):
        refresh_pub_from_git()
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        local_host = is_local(self.request.get_host())
        kwargs = select_blog_doc(pub, doc, local_host)
        return kwargs
