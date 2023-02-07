from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from publish.slides import slides_view_context

# from publish.book import book_context

from .pub import get_host, select_blog_doc
from .pub import pub_redirect
from .models import Pub


class BlogTodayView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.path.replace("today", localtime().strftime("%m-%d"))


class PubRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        host = get_host(self.request)
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", 'Index.md')
        return pub_redirect(host, pub, doc)


class PubView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        blog = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(host, blog, doc)
        return kwargs


class PubListView(TemplateView):
    template_name = "blog/list.html"
    model = Pub
    context_object_name = "pubs"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        pub = self.kwargs.get('pub')
        kwargs = select_blog_doc(host, 'sampler',  "Index.md")
        kwargs['pubs'] = Pub.objects.filter(pub_type=pub)
        # kwargs = super().get_context_data(**kwargs)
        return kwargs


class PubDetailView(TemplateView):
    template_name = "pub/cover.html"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        blog = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        kwargs = select_blog_doc(host, blog, doc)
        return kwargs


class PubCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/add.html"
    model = Pub
    fields = "__all__"


class PubUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "blog/edit.html"
    model = Pub
    fields = "__all__"


class PubDeleteView(LoginRequiredMixin, DeleteView):
    model = Pub
    template_name = "blog/delete.html"
    success_url = reverse_lazy("blog_list")


class TweetView(TemplateView):
    template_name = "tweet.html"

    def get_context_data(self, **kwargs):
        host = get_host(self.request)
        host = "shrinking-world.com"
        blog = "tweet"
        doc = str(kwargs.get("tweet"))
        return select_blog_doc(host, blog, doc)


class RandomTweetView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        host = get_host(self.request)
        host = "shrinking-world.com"
        blog = "tweet"
        page = "random"
        return pub_redirect(host, blog, page)


class SlidesShowView(TemplateView):
    template_name = 'course_slides.html'

    def get_context_data(self, **kwargs):
        return slides_view_context(**kwargs)
