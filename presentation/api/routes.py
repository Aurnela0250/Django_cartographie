from ninja_extra import NinjaExtraAPI

from presentation.api.exception_handlers import global_exception_handler
from presentation.api.v1.auth_controller import AuthController
from presentation.api.v1.school_controller import SchoolController
from presentation.api.v1.school_year_controller import SchoolYearController

api = NinjaExtraAPI()

api.register_controllers(AuthController)
api.register_controllers(SchoolController)
api.register_controllers(SchoolYearController)
api.add_exception_handler(Exception, global_exception_handler)
