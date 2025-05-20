from django.urls import path

# Importer les contrôleurs par version
from presentation.api.v1.router import api as api_v1

routes = [
    path("v1/", api_v1.urls),
]
