from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    #
    # Admin
    path("admin/", admin.site.urls),
    #
    # Accounts
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('doc.urls_accounts')),
    # Task
    path("", include("task.urls")),
    #
    # Hammer Test
    # path('', TestView.as_view()),
    path("test/", include("probe.urls_probe")),
    #
    # Workshop
    # path("views/", include("workshop.urls_views")),
    # path("factory/", include("workshop.urls_factory")),
    #
    # Course
    path("", include("course.urls")),
    #
    # Book & Blogs
    path("", include("publish.urls")),
]
