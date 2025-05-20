"""
Initialisation personnalisée pour Django Ninja.
Ce fichier est importé avant que Django Ninja ne soit initialisé.
"""
import warnings
from django.utils.deprecation import RemovedInDjango60Warning
from pydantic._internal._config import PydanticDeprecatedSince20

# Filtrer l'avertissement spécifique concernant le convertisseur 'uuid'
warnings.filterwarnings(
    "ignore",
    message="Converter 'uuid' is already registered. Support for overriding registered converters is deprecated and will be removed in Django 6.0.",
    category=RemovedInDjango60Warning,
)

# Filtrer l'avertissement de Pydantic concernant la configuration basée sur les classes
warnings.filterwarnings(
    "ignore",
    message="Support for class-based `config` is deprecated, use ConfigDict instead",
    category=PydanticDeprecatedSince20,
)