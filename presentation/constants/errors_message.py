"""
This module contains constants for error messages used in the application.
These messages are used to provide user-friendly feedback for various error scenarios.
"""

# 4xx Client Errors
BAD_REQUEST = "Invalid request. Check required fields and try again."
UNPROCESSABLE_ENTITY = "Request failed validation. Check your data and try again."
UNAUTHORIZED = "Access denied. Authentication required."
FORBIDDEN = "Access forbidden. Insufficient permissions."
NOT_FOUND = "Resource not found."
CONFLICT = "A conflict occurred. The resource already exists."
TOO_MANY_REQUESTS = "Too many requests. Wait before trying again."

# 5xx Server Errors
INTERNAL_SERVER_ERROR = "Server error. Please try again later."
SERVICE_UNAVAILABLE = "Service temporarily unavailable. Try again later."

# Custom Errors
VALIDATION_ERROR = "Validation failed. Please check the provided data and try again."
INVALID_CREDENTIALS = "The provided credentials are invalid. Please try again."
AUTHENTICATION_ERROR = "Authentication failed. Please verify your credentials."
INVALID_TOKEN = "The token is invalid or has expired or revoked. Please log in again."
DATABASE_ERROR = (
    "A database error occurred. Please contact support if the issue persists."
)
EXTERNAL_SERVICE_ERROR = "An error occurred while communicating with an external service. Please try again later."
