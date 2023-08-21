from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Accounts
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('doc.urls_accounts')),

    # Task
    path("", include("task.urls")),

    # Course
    path("", include("course.urls")),

    # Hammer Test
    path("test/", include("probe.urls_probe")),

    # Writer
    path("writer/", include("writer.urls")),

    # Book & Blogs
    path("", include("publish.urls")),
]
