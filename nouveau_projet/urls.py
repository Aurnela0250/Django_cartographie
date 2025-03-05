"""
URL configuration for nouveau_projet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cartographie import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cartographie.urls')),
    # etablissement
    path('liste/', views.liste_etablissements, name='liste_etablissements'),
    path('creer/', views.creer_etablissement, name='creer_etablissement'),
    path('modifier/<int:id>/', views.modifier_etablissement, name='modifier_etablissement'),
    path('supprimer/<int:id>/', views.supprimer_etablissement, name='supprimer_etablissement'),
    # Utilisateur
    path('creerUtilisateur/', views.creer_utilisateur, name='creer_utilisateur'),
    path('listeUtilisateur/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('modifierUtilisateur/<int:pk>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('supprimerUtilisateur/<int:pk>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('connexionUtilisateur/', views.connexion, name='connexion'),
]