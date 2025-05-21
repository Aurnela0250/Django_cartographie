import functools
from typing import Callable, Optional, Type

from pydantic import BaseModel


# Utilisation : @cache_response(cache_service, cache_type="item" ou "list", ...)
def cache_response(
    cache_service,
    cache_type: str = "item",  # "item" ou "list"
    schema_type: Optional[Type[BaseModel]] = None,
    get_id: Optional[Callable] = None,  # Pour cache_type="item"
    get_pagination: Optional[Callable] = None,  # Pour cache_type="list"
    get_filter_str: Optional[Callable] = None,  # Pour cache_type="list"
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Récupérer l'instance réelle du cache_service si c'est une fonction (lambda)
            cs = (
                cache_service(*args, **kwargs)
                if callable(cache_service)
                else cache_service
            )
            # Pour les détails (item)
            if cache_type == "item":
                item_id = get_id(*args, **kwargs) if get_id else kwargs.get("id")
                cached = cs.get_item(item_id, schema_type)
                if cached:
                    return cached
                result = func(*args, **kwargs)
                if result:
                    cs.set_item(item_id, result)
                return result
            # Pour les listes paginées
            elif cache_type == "list":
                pagination_params = (
                    get_pagination(*args, **kwargs)
                    if get_pagination
                    else kwargs.get("pagination_params")
                )
                filter_str = get_filter_str(*args, **kwargs) if get_filter_str else None
                cached = cs.get_paginated_list(
                    pagination_params=pagination_params,
                    response_schema_type=schema_type,
                    filter_str=filter_str,
                )
                if cached:
                    return cached
                result = func(*args, **kwargs)
                if result:
                    cs.set_paginated_list(
                        pagination_params=pagination_params,
                        data=result,
                        filter_str=filter_str,
                    )
                return result
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
