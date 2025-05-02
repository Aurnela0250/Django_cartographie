from ninja_extra import NinjaExtraAPI

from presentation.api.exception_handlers import global_exception_handler

# Importer les contrôleurs par version
from .endpoints.auth_controller import AuthController
from .endpoints.domain_controller import DomainController
from .endpoints.level_controller import LevelController
from .endpoints.region_controller import RegionController

controllers = [AuthController, RegionController, LevelController, DomainController]

# Création de l'API
api = NinjaExtraAPI(
    title="API Cartographie",
    version="1.0.0",
    description="""
        API pour la gestion de la cartographie des données.
        
        Cette API permet de gérer les données cartographiques, les utilisateurs et leurs autorisations.
        Elle fournit des endpoints pour l'authentification, la gestion des profils utilisateurs,
        et la manipulation des données cartographiques.
        
        Le versionnement de l'API est géré via des préfixes d'URL (/api/v1/, /api/v2/, etc.).
        
        ## Versions disponibles
        - **v1** : Version initiale de l'API (actuelle)
        - **v2** : Version future avec fonctionnalités améliorées (en développement)
    """,
)

# Enregistrer les contrôleurs
api.register_controllers(*controllers)

# Configuration globale des gestionnaires d'exceptions
api.add_exception_handler(Exception, global_exception_handler)
