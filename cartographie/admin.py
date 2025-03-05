from django.contrib import admin
from .models import Etablissement, Role, Utilisateur

# Register your models here.
# admin.site.register(Etablissement)

class EtablissementAdmin(admin.ModelAdmin):
    # Colonnes à afficher dans la liste
    list_display = ('nom', 'type', 'latitude', 'longitude')
    
    # Champs sur lesquels on peut effectuer une recherche
    search_fields = ('nom', 'type')
    
    # Filtres dans la barre latérale
    list_filter = ('type',)
    
    # Nombre d'éléments par page
    list_per_page = 20
    
    # Champs pour l'édition groupés en sections
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'type', 'description')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude')
        }),
    )


class RoleAdmin(admin.ModelAdmin):
    # Colonnes à afficher dans la liste
    list_display_r = ('nomRole')
    
    # Champs sur lesquels on peut effectuer une recherche
    search_fields_r = ('nomRole',)
    
    # Nombre d'éléments par page
    list_per_page_r = 20

class UtilisateurAdmin(admin.ModelAdmin):
    # Colonnes à afficher dans la liste
    list_display = ('nom', 'prenom', 'email', 'mot_de_passe', 'role')
    
    # Champs sur lesquels on peut effectuer une recherche
    search_fields = ('nom', 'prenom', 'email', 'mot_de_passe', 'role')
    
    # Filtres dans la barre latérale
    list_filter = ('role',)
    
    # Nombre d'éléments par page
    list_per_page = 20
    
    # Champs pour l'édition groupés en sections
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'prenom', 'email')
        }),
    )

# Enregistrer le modèle avec la classe d'administration personnalisée
admin.site.register(Etablissement, EtablissementAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)