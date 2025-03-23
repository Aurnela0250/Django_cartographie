from typing import List
from uuid import UUID

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.use_cases.school_use_case import (
    CreateSchoolUseCase,
    DeleteSchoolUseCase,
    GetAllSchoolsUseCase,
    GetSchoolUseCase,
    UpdateSchoolUseCase,
)
from infrastructure.db.django_school_repository import DjangoSchoolRepository
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    BadRequestError,
    ValidationError,
)
from presentation.schemas.school_schema import CreateSchoolSchema as SchoolCreate
from presentation.schemas.school_schema import SchoolSchema as SchoolOut
from presentation.schemas.school_schema import UpdateSchoolSchema as SchoolUpdate


@api_controller("/schools", tags=["Schools"], auth=jwt_auth)
class SchoolController:
    def __init__(self):
        self.school_repository = DjangoSchoolRepository()

    @http_post("/", response={201: SchoolOut})
    def create_school(self, request, school_data: SchoolCreate):
        try:

            use_case = CreateSchoolUseCase(self.school_repository)
            school = use_case.execute(
                school_data.dict(),
                created_by=request.user.id,
            )
            return 201, SchoolOut.from_orm(school)
        except BadRequestError as e:
            raise e
        except ValidationError as e:
            return e
        except Exception as e:
            raise e

    @http_get("/{school_id}", response=SchoolOut)
    def get_school(self, request, school_id: UUID):
        use_case = GetSchoolUseCase(self.school_repository)
        school = use_case.execute(school_id)
        return SchoolOut.from_orm(school)

    @http_get("/", response=List[SchoolOut])
    def get_all_schools(self):
        use_case = GetAllSchoolsUseCase(self.school_repository)
        schools = use_case.execute()
        return [SchoolOut.from_orm(school) for school in schools]

    @http_put("/{school_id}", response=SchoolOut)
    def update_school(self, request, school_id: UUID, school_data: SchoolUpdate):
        try:
            use_case = UpdateSchoolUseCase(self.school_repository)
            updated_school = use_case.execute(
                school_id,
                school_data.dict(exclude_unset=True),
                updated_by=request.user.id,
            )
            return SchoolOut.from_orm(updated_school)
        except ValidationError as e:
            raise BadRequestError(detail=str(e))

    @http_delete("/{school_id}", response={204: None})
    def delete_school(self, school_id: UUID):
        use_case = DeleteSchoolUseCase(self.school_repository)
        use_case.execute(school_id)
        return 204, None
