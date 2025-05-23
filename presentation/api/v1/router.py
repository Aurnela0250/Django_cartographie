from ninja import Swagger
from ninja_extra import NinjaExtraAPI

from presentation.api.v1.endpoints.chat_controller import ChatController
from presentation.api.exception_handlers import global_exception_handler

# Importer les contrôleurs par version
from .endpoints.auth_controller import AuthController
from .endpoints.city_controller import CityController
from .endpoints.domain_controller import DomainController
from .endpoints.establishment_controller import EstablishmentController
from .endpoints.establishment_type_controller import EstablishmentTypeController
from .endpoints.formation_controller import FormationController
from .endpoints.level_controller import LevelController
from .endpoints.mention_controller import MentionController
from .endpoints.region_controller import RegionController
from .endpoints.sector_controller import SectorController

controllers = [
    AuthController,
    RegionController,
    LevelController,
    DomainController,
    MentionController,
    EstablishmentTypeController,
    EstablishmentController,
    SectorController,
    FormationController,
    CityController,
    ChatController,
]

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
    docs=Swagger(settings={"persistAuthorization": True, "filter": True}),
)


# Enregistrer les contrôleurs
api.register_controllers(*controllers)

# Configuration globale des gestionnaires d'exceptions
api.add_exception_handler(Exception, global_exception_handler)
