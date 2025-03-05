from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilisateurViewSet
from .views import EtablissementViewSet


router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)
router.register(r'etablissements', EtablissementViewSet)


urlpatterns = [
    path('', views.carte, name='carte'),
    path('api/', include(router.urls)),
]

