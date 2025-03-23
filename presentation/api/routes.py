from ninja_extra import NinjaExtraAPI

from presentation.api.exception_handlers import global_exception_handler
from presentation.api.v1.auth_controller import AuthController

api = NinjaExtraAPI()

api.register_controllers(AuthController)
api.add_exception_handler(Exception, global_exception_handler)
