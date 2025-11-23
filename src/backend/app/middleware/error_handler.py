"""
Error handling middleware for the healthcare API.

This module provides centralized error handling for all API endpoints,
ensuring consistent error responses and proper HTTP status codes.

Requirements: 6.1, 6.2, 7.1, 7.2, 7.3, 8.1, 8.2, 8.3, 8.4, 8.5
"""

import logging
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import OperationalError, DatabaseError, IntegrityError
from pydantic import ValidationError

from app.schemas.responses import ErrorResponse

logger = logging.getLogger(__name__)


def sanitize_error_message(error_msg: str) -> str:
    """
    Remove sensitive information from error messages.
    
    Ensures credentials, passwords, and other sensitive data are never
    exposed in error responses.
    
    Requirements: 7.3
    """
    import os
    
    sensitive_patterns = [
        os.getenv("DB_PASSWORD", ""),
        os.getenv("DB_USER", ""),
        "password=",
        "pwd=",
        "token=",
        "api_key=",
        "secret=",
    ]
    
    sanitized = error_msg
    for pattern in sensitive_patterns:
        if pattern and pattern in sanitized.lower():
            # Replace the entire credential value
            sanitized = sanitized.replace(pattern, "[REDACTED]")
    
    return sanitized


async def error_handler_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware to catch and handle all exceptions in a centralized manner.
    
    This middleware ensures:
    - Database connection errors return HTTP 503
    - Validation errors return HTTP 400 with details
    - Not found errors return HTTP 404
    - Unexpected errors return HTTP 500
    - All error responses follow ErrorResponse schema
    - Credentials and sensitive data are never exposed
    
    Requirements: 6.1, 6.2, 7.1, 7.2, 7.3, 8.1, 8.2, 8.3, 8.4, 8.5
    """
    try:
        response = await call_next(request)
        return response
        
    except StarletteHTTPException as exc:
        # Handle HTTP exceptions (including 404, 400, etc.)
        # These are already properly formatted by route handlers
        logger.warning(
            f"HTTP exception: {exc.status_code} - {exc.detail}",
            extra={
                "status_code": exc.status_code,
                "path": request.url.path,
                "method": request.method,
            }
        )
        
        # If detail is already a dict (our error format), use it directly
        if isinstance(exc.detail, dict):
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail
            )
        
        # Otherwise, wrap it in our error format
        error_response = ErrorResponse.create(
            code="HTTP_ERROR",
            message=str(exc.detail)
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )
    
    except RequestValidationError as exc:
        # Handle Pydantic validation errors from request parameters
        # Requirements: 6.1, 6.2, 8.3
        logger.warning(
            f"Validation error: {exc}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors(),
            }
        )
        
        error_response = ErrorResponse.create(
            code="VALIDATION_ERROR",
            message="Invalid request parameters",
            details={
                "errors": exc.errors()
            }
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    except ValidationError as exc:
        # Handle Pydantic validation errors from response models
        # Requirements: 6.1, 6.2, 8.3
        logger.warning(
            f"Response validation error: {exc}",
            extra={
                "path": request.url.path,
                "method": request.method,
            }
        )
        
        error_response = ErrorResponse.create(
            code="VALIDATION_ERROR",
            message="Invalid data format",
            details={
                "errors": exc.errors()
            }
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    except (OperationalError, DatabaseError) as exc:
        # Handle database connection and operational errors
        # Requirements: 7.1, 7.2, 7.3, 8.1
        sanitized_msg = sanitize_error_message(str(exc))
        
        logger.error(
            f"Database error: {sanitized_msg}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__,
            },
            exc_info=True
        )
        
        error_response = ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Service temporarily unavailable. Please try again later."
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=error_response.model_dump()
        )
    
    except IntegrityError as exc:
        # Handle database integrity errors (constraint violations, etc.)
        # Requirements: 7.1, 7.3, 8.3
        sanitized_msg = sanitize_error_message(str(exc))
        
        logger.error(
            f"Database integrity error: {sanitized_msg}",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
            exc_info=True
        )
        
        error_response = ErrorResponse.create(
            code="INTEGRITY_ERROR",
            message="Data integrity constraint violation"
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump()
        )
    
    except RuntimeError as exc:
        # Handle runtime errors (like database not initialized)
        # Requirements: 7.1, 8.1
        sanitized_msg = sanitize_error_message(str(exc))
        
        logger.error(
            f"Runtime error: {sanitized_msg}",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
            exc_info=True
        )
        
        error_response = ErrorResponse.create(
            code="SERVICE_ERROR",
            message="Service temporarily unavailable"
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=error_response.model_dump()
        )
    
    except Exception as exc:
        # Catch-all for unexpected errors
        # Requirements: 7.3, 8.4
        sanitized_msg = sanitize_error_message(str(exc))
        
        logger.error(
            f"Unexpected error: {sanitized_msg}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__,
            },
            exc_info=True
        )
        
        error_response = ErrorResponse.create(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later."
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump()
        )


class NotFoundError(Exception):
    """
    Custom exception for resource not found errors.
    
    Raises HTTP 404 when caught by error handler middleware.
    Requirements: 8.2
    """
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)
