# Error response examples for API endpoints
from typing import Any, Dict

error_500_response = {
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erreur interne du serveur.",
                    "code": "internal_server",
                    "category": "server_error",
                    "request_id": "req-999999",
                    "timestamp": "2023-10-01T12:00:00Z",
                    "details": None,
                    "stack_trace": "Traceback (most recent call last): ...",
                },
            },
        },
    },
}

error_422_response = {
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erreur de validation.",
                    "code": "validation",
                    "category": "client_error",
                    "request_id": "req-654321",
                    "timestamp": "2023-10-01T12:00:00Z",
                    "details": [
                        {
                            "field": "email",
                            "message": "Format d'email invalide.",
                            "code": "bad_request",
                            "value": "not-an-email",
                        }
                    ],
                    "stack_trace": None,
                },
            },
        },
    },
}
error_401_response = {
    401: {
        "description": "Authentication error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Access denied. Authentication required.",
                    "code": "unauthorized",
                    "category": "client_error",
                    "request_id": "req-123456",
                    "timestamp": "2023-10-01T12:00:00Z",
                    "details": None,
                    "stack_trace": None,
                },
            },
        },
    },
}
error_400_response = {
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                    "message": "Requête invalide.",
                    "code": "bad_request",
                    "category": "client_error",
                    "request_id": "req-400400",
                    "timestamp": "2023-10-01T12:00:00Z",
                    "details": None,
                    "stack_trace": None,
                },
            },
        },
    },
}

error_404_response = {
    404: {
        "description": "Resource not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "Ressource non trouvée.",
                    "code": "not_found",
                    "category": "client_error",
                    "request_id": "req-404404",
                    "timestamp": "2023-10-01T12:00:00Z",
                    "details": None,
                    "stack_trace": None,
                },
            },
        },
    },
}

error_409_response = {
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {
                "example": {
                    "message": "Conflit détecté.",
                    "code": "conflict",
                    "category": "client_error",
                    "request_id": "req-409409",
                    "timestamp": "2023-10-01T12:00:00Z",
                    "details": None,
                    "stack_trace": None,
                },
            },
        },
    },
}

# Response endpoints
sign_up_responses: Dict[int | str, Dict[str, Any]] = {
    201: {
        "description": "User created successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "email": "user@example.com",
                    "active": True,
                    "created_by": None,
                    "updated_by": None,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                },
            },
        },
    },
    **error_500_response,
}

login_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "Login successful",
        "content": {
            "application/json": {
                "example": {
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "active": True,
                        "created_by": None,
                        "updated_by": None,
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": "2023-10-01T12:00:00Z",
                    },
                    "user_id": "1",
                    "exp": 1710000000,
                    "iat": 1709990000,
                    "jti": "jwt-uuid-123",
                    "token_type": "access",
                    "iss": "your-issuer",
                    "aud": "your-audience",
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                },
            },
        },
    },
    **error_422_response,
}

refresh_token_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "Refresh successful",
        "content": {
            "application/json": {
                "example": {
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "active": True,
                        "created_by": None,
                        "updated_by": None,
                        "created_at": "2023-10-01T12:00:00Z",
                        "updated_at": "2023-10-01T12:00:00Z",
                    },
                    "user_id": "1",
                    "exp": 1710000000,
                    "iat": 1709990000,
                    "jti": "jwt-uuid-123",
                    "token_type": "access",
                    "iss": "your-issuer",
                    "aud": "your-audience",
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                },
            },
        },
    },
    **error_422_response,
    **error_401_response,
    **error_500_response,
}


# Réponse pour l'endpoint /logout
logout_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "Logout successful",
        "content": {
            "application/json": {
                "example": {"message": "Successfully logged out"},
            },
        },
    },
    **error_401_response,
    **error_500_response,
}

# Réponse pour l'endpoint /me
current_user_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "Current user details",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "email": "user@example.com",
                    "active": True,
                    "created_by": None,
                    "updated_by": None,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                },
            },
        },
    },
    **error_401_response,
    **error_500_response,
}

# Réponses pour les endpoints de villes (Cities)

# Endpoint POST /cities/ - Créer une ville
create_city_responses: Dict[int | str, Dict[str, Any]] = {
    201: {
        "description": "City created successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Paris",
                    "region_id": 1,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                    "created_by": 1,
                    "updated_by": None,
                },
            },
        },
    },
    **error_401_response,
    **error_409_response,
    **error_422_response,
    **error_500_response,
}

# Endpoint GET /cities/{city_id}/ - Récupérer une ville
get_city_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "City details",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Paris",
                    "region_id": 1,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                    "created_by": 1,
                    "updated_by": None,
                },
            },
        },
    },
    **error_401_response,
    **error_404_response,
    **error_500_response,
}

# Endpoint GET /cities/ - Lister toutes les villes (paginé)
get_all_cities_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "Paginated list of cities",
        "content": {
            "application/json": {
                "example": {
                    "items": [
                        {
                            "id": 1,
                            "name": "Paris",
                            "region_id": 1,
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": "2023-10-01T12:00:00Z",
                            "created_by": 1,
                            "updated_by": None,
                        },
                        {
                            "id": 2,
                            "name": "Lyon",
                            "region_id": 2,
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": "2023-10-01T12:00:00Z",
                            "created_by": 1,
                            "updated_by": None,
                        },
                    ],
                    "total_items": 2,
                    "page": 1,
                    "per_page": 10,
                    "total_pages": 1,
                    "next_page": None,
                    "previous_page": None,
                },
            },
        },
    },
    **error_401_response,
    **error_422_response,
    **error_500_response,
}

# Endpoint PUT /cities/{city_id}/ - Modifier une ville
update_city_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "City updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Paris Modifié",
                    "region_id": 1,
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:30:00Z",
                    "created_by": 1,
                    "updated_by": 1,
                },
            },
        },
    },
    **error_401_response,
    **error_404_response,
    **error_409_response,
    **error_422_response,
    **error_500_response,
}

# Endpoint DELETE /cities/{city_id}/ - Supprimer une ville
delete_city_responses: Dict[int | str, Dict[str, Any]] = {
    204: {
        "description": "City deleted successfully",
    },
    **error_401_response,
    **error_404_response,
    **error_500_response,
}

# Endpoint GET /cities/filter/ - Filtrer les villes (paginé)
filter_cities_responses: Dict[int | str, Dict[str, Any]] = {
    200: {
        "description": "Filtered paginated list of cities",
        "content": {
            "application/json": {
                "example": {
                    "items": [
                        {
                            "id": 1,
                            "name": "Paris",
                            "region_id": 1,
                            "created_at": "2023-10-01T12:00:00Z",
                            "updated_at": "2023-10-01T12:00:00Z",
                            "created_by": 1,
                            "updated_by": None,
                        },
                    ],
                    "total_items": 1,
                    "page": 1,
                    "per_page": 10,
                    "total_pages": 1,
                    "next_page": None,
                    "previous_page": None,
                },
            },
        },
    },
    **error_401_response,
    **error_422_response,
    **error_500_response,
}
