# Importer les contrôleurs par version
from fastapi import APIRouter

from .endpoints.auth_controller import router as auth_router
from .endpoints.city_controller import router as city_router
from .endpoints.domain_controller import router as domain_router
from .endpoints.establishment_controller import router as establishment_router
from .endpoints.establishment_type_controller import router as establishment_type_router
from .endpoints.formation_controller import router as formation_router
from .endpoints.level_controller import router as level_router
from .endpoints.mention_controller import router as mention_router
from .endpoints.region_controller import router as region_router

# Router parent avec le préfixe global v1
v1_router = APIRouter(prefix="/v1")


v1_router.include_router(auth_router)
v1_router.include_router(city_router)
v1_router.include_router(domain_router)
v1_router.include_router(establishment_router)
v1_router.include_router(establishment_type_router)
v1_router.include_router(formation_router)
v1_router.include_router(level_router)
v1_router.include_router(mention_router)
v1_router.include_router(region_router)
