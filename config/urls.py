from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from presentation.api.routes import routes

urlpatterns = [
    path("admin/", admin.site.urls),
    # Route principale de l'API avec versionnement intégré
    path("api/", include(routes)),
    # Redirection vers la documentation de l'API
    path("", lambda request: redirect("api/v1/docs"), name="redirect-to-docs"),
]
