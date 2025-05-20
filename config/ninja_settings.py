"""
Configuration spécifique pour Django Ninja.
"""

# Désactiver l'enregistrement automatique du convertisseur UUID
# pour éviter l'avertissement de Django 6.0
NINJA_SKIP_REGISTRY_UUID_CONVERTER = True