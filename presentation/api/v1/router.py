# Importer les contrôleurs par version
from .endpoints.auth_controller import router as auth_router

routers = [
    auth_router,
]
