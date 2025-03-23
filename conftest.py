"""
Configuration pytest pour Django.
"""
import os
import warnings

from django.utils.deprecation import RemovedInDjango60Warning
from pydantic._internal._config import PydanticDeprecatedSince20

# Configuration de Django pour pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Filtrer les avertissements spécifiques
warnings.filterwarnings(
    "ignore",
    message="Converter 'uuid' is already registered. Support for overriding registered converters is deprecated and will be removed in Django 6.0.",
    category=RemovedInDjango60Warning,
)

warnings.filterwarnings(
    "ignore",
    message="Support for class-based `config` is deprecated, use ConfigDict instead",
    category=PydanticDeprecatedSince20,
)