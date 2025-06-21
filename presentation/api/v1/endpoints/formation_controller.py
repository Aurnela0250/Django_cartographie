from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.filters import FormationFilters
from core.entities.formation import FormationEntity
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.formation_use_case import FormationUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.formation import (
    CreateFormationSchema,
    FormationSchema,
    UpdateFormationSchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/formations",
    tags=["Formations"],
)


@router.post(
    "/",
    response_model=FormationSchema,
    status_code=201,
)
@inject
async def create(
    *,
    formation_data: CreateFormationSchema,
    formation_use_case: FormationUseCase = Depends(
        Provide[Container.formation_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = FormationEntity(**formation_data.model_dump(), created_by=user.id)
        created = await formation_use_case.create(entity)
        return FormationSchema.model_validate(created)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{formation_id}/",
    response_model=FormationSchema,
    status_code=200,
)
@inject
async def get(
    *,
    formation_id: int = Path(..., title="ID de la formation", gt=0),
    formation_use_case: FormationUseCase = Depends(
        Provide[Container.formation_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        formation = await formation_use_case.get(formation_id)
        return FormationSchema.model_validate(formation)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[FormationSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    formation_use_case: FormationUseCase = Depends(
        Provide[Container.formation_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await formation_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        FormationSchema,
        FormationSchema.model_validate,
    )


@router.put(
    "/{formation_id}/",
    response_model=FormationSchema,
    status_code=200,
)
@inject
async def update(
    *,
    formation_id: int = Path(..., title="ID de la formation", gt=0),
    formation_data: UpdateFormationSchema,
    formation_use_case: FormationUseCase = Depends(
        Provide[Container.formation_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = FormationEntity(
            **formation_data.model_dump(),
            updated_by=user.id,
        )
        updated = await formation_use_case.update(formation_id, entity)
        return FormationSchema.model_validate(updated)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{formation_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    formation_id: int = Path(..., title="ID de la formation", gt=0),
    formation_use_case: FormationUseCase = Depends(
        Provide[Container.formation_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await formation_use_case.delete(formation_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[FormationSchema],
    status_code=200,
)
@inject
async def filter(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    filters: Annotated[
        FormationFilters,
        Query(),
    ],
    formation_use_case: FormationUseCase = Depends(
        Provide[Container.formation_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await formation_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        FormationSchema,
        FormationSchema.model_validate,
    )

    # @http_post(
    #     "/{formation_id}/authorization",
    #     response=FormationSchema,
    # )
    # def create_authorization(
    #     self,
    #     request,
    #     formation_id: int,
    #     authorization_data: CreateFormationAuthorizationSchema,
    # ):
    #     """Create an authorization for a formation"""
    #     try:
    #         entity_data = FormationAuthorizationEntity(
    #             **authorization_data.model_dump(),
    #             created_by=request.auth.get("user_id"),
    #         )

    #         formation = self.formation_use_case.create_authorization(
    #             formation_id, entity_data
    #         )

    #         return FormationSchema.from_orm(formation)
    #     except NotFoundError as e:
    #         raise e
    #     except ValidationError as e:
    #         raise e
    #     except DatabaseError as e:
    #         raise e
    #     except Exception:
    #         raise InternalServerError()

    # @http_put("/{formation_id}/authorization", response=FormationSchema)
    # def update_authorization(
    #     self,
    #     request,
    #     formation_id: int,
    #     authorization_data: UpdateFormationAuthorizationSchema,
    # ):
    #     """Update the authorization of a formation"""
    #     try:
    #         # Get the existing formation first
    #         current_formation = self.formation_use_case.get_formation(formation_id)

    #         if not current_formation.authorization:
    #             raise NotFoundError()

    #         # Update with new data, keeping existing values for fields not in the update
    #         auth_update_data = current_formation.authorization.model_dump()
    #         auth_update_data.update(authorization_data.model_dump(exclude_unset=True))
    #         auth_update_data["updated_by"] = request.auth.get("user_id")

    #         entity_to_update = FormationAuthorizationEntity(**auth_update_data)

    #         updated_formation = self.formation_use_case.update_authorization(
    #             formation_id, entity_to_update
    #         )
    #         return FormationSchema.from_orm(updated_formation)
    #     except NotFoundError as e:
    #         raise e
    #     except ValidationError as e:
    #         raise e
    #     except DatabaseError as e:
    #         raise e
    #     except Exception:
    #         raise InternalServerError()

    # @http_post("/{formation_id}/annual-headcount", response={201: FormationSchema})
    # def add_annual_headcount(
    #     self,
    #     request,
    #     formation_id: int,
    #     headcount_data: AnnualHeadcountCreate,
    # ):
    #     """Ajoute un effectif annuel à une formation"""
    #     try:
    #         entity_data = AnnualHeadCountEntity(
    #             **headcount_data.model_dump(),
    #             formation_id=formation_id,
    #             created_by=request.auth.get("user_id"),
    #             updated_by=request.auth.get("user_id"),
    #         )

    #         formation = self.formation_use_case.add_annual_headcount(
    #             formation_id, entity_data
    #         )
    #         return 201, FormationSchema.from_orm(formation)
    #     except NotFoundError as e:
    #         raise e
    #     except ConflictError as e:
    #         raise e
    #     except ValidationError as e:
    #         raise e
    #     except DatabaseError as e:
    #         raise e
    #     except Exception:
    #         raise InternalServerError()

    # @http_put(
    #     "{formation_id}/annual-headcount/{annual_headcount_id}",
    #     response=FormationSchema,
    # )
    # def update_annual_headcount(
    #     self,
    #     request,
    #     formation_id: int,
    #     annual_headcount_id: int,
    #     headcount_data: AnnualHeadcountUpdate,
    # ):
    #     """Met à jour un effectif annuel existant"""
    #     try:
    #         # Convertir directement les données de la requête en entité
    #         # La vérification de l'existence sera faite dans le use case
    #         entity_data = AnnualHeadCountEntity(
    #             id=annual_headcount_id,
    #             **headcount_data.model_dump(exclude_unset=True),
    #             formation_id=formation_id,
    #             updated_by=request.auth.get("user_id"),
    #         )

    #         # Mettre à jour l'effectif annuel via le use case
    #         updated_formation = self.formation_use_case.update_annual_headcount(
    #             annual_headcount_id, entity_data
    #         )
    #         return FormationSchema.from_orm(updated_formation)
    #     except NotFoundError as e:
    #         raise e
    #     except ConflictError as e:
    #         raise e
    #     except ValidationError as e:
    #         raise e
    #     except DatabaseError as e:
    #         raise e
    #     except Exception:
    #         self.logger.error("An unexpected error occurred", exc_info=True)
    #         raise InternalServerError()

    # @http_delete(
    #     "{formation_id}/annual-headcount/{annual_headcount_id}", response={204: None}
    # )
    # def delete_annual_headcount(
    #     self,
    #     formation_id: int,
    #     annual_headcount_id: int,
    # ):
    #     """Supprime un effectif annuel"""
    #     try:
    #         self.formation_use_case.delete_annual_headcount(annual_headcount_id)
    #         return 204, None
    #     except NotFoundError as e:
    #         raise e
    #     except Exception:
    #         raise InternalServerError()
