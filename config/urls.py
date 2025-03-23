from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from presentation.api.routes import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", lambda request: redirect("api/docs"), name="redirect-to-docs"),
]
