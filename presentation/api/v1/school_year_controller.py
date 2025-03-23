from typing import List

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.use_cases.school_year_use_case import SchoolYearUseCase
from infrastructure.db.django_school_year_repository import DjangoSchoolYearRepository
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import BadRequestError, NotFoundError, ValidationError
from presentation.schemas.school_year_schema import (
    CreateSchoolYearSchema as SchoolYearCreate,
)
from presentation.schemas.school_year_schema import SchoolYearSchema as SchoolYearOut
from presentation.schemas.school_year_schema import (
    UpdateSchoolYearSchema as SchoolYearUpdate,
)


@api_controller("/school_years", tags=["School Years"], auth=jwt_auth)
class SchoolYearController:
    def __init__(self):
        self.school_year_repository = DjangoSchoolYearRepository()

    @http_post("/", response={201: SchoolYearOut})
    def create_school_year(self, request, school_year_data: SchoolYearCreate):
        try:
            use_case = SchoolYearUseCase(self.school_year_repository)
            school_year = use_case.create(
                school_year_data.dict(),
                created_by=request.user.id,
            )
            return 201, SchoolYearOut.from_orm(school_year)
        except BadRequestError as e:
            raise e
        except ValidationError as e:
            return e
        except Exception as e:
            raise e

    @http_get("/{school_year_id}", response=SchoolYearOut)
    def get_school_year(self, request, school_year_id: int):
        try:
            use_case = SchoolYearUseCase(self.school_year_repository)
            school_year = use_case.get(school_year_id)
            return SchoolYearOut.from_orm(school_year)
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise e

    @http_get("/", response=List[SchoolYearOut])
    def get_all_school_years(self):
        try:
            use_case = SchoolYearUseCase(self.school_year_repository)
            school_years = use_case.get_all()
            return [SchoolYearOut.from_orm(school_year) for school_year in school_years]
        except Exception as e:
            raise e

    @http_put("/{school_year_id}", response=SchoolYearOut)
    def update_school_year(
        self,
        request,
        school_year_id: int,
        school_year_data: SchoolYearUpdate,
    ):
        try:
            use_case = SchoolYearUseCase(self.school_year_repository)
            updated_school_year = use_case.update(
                school_year_id,
                school_year_data.dict(exclude_unset=True),
                updated_by=request.user.id,
            )
            return SchoolYearOut.from_orm(updated_school_year)
        except BadRequestError as e:
            raise e
        except ValidationError as e:
            raise e
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise BadRequestError(detail=str(e))

    @http_delete("/{school_year_id}", response={204: None})
    def delete_school_year(self, request, school_year_id: int):
        try:
            use_case = SchoolYearUseCase(self.school_year_repository)
            use_case.delete(school_year_id)
            return 204, None
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise e
