"""
Initialisation du package config.
"""
# Importer l'initialisation personnalisée pour Django Ninja
try:
    from config.ninja_init import *
except ImportError:
    pass