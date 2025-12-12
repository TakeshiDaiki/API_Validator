"""
Personal Data Validator API using FastAPI.

Endpoints:
    POST /validate - Validate personal data for a user
    GET / - API information
    GET /docs - Interactive Swagger UI
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.models import UsuarioValidation

# ==================== LOGGING CONFIGURATION ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== GLOBAL ERROR HANDLER ====================
def format_validation_errors(errors: list) -> Dict[str, str]:
    """Format Pydantic validation errors into a friendly dict."""
    error_dict = {}
    for error in errors:
        field = error['loc'][0] if error['loc'] else 'general'
        message = error['msg']

        # Normalize known messages
        if 'at least 2 characters' in message:
            message = 'Must have at least 2 characters'

        error_dict[str(field)] = message

    return error_dict
# ==================== LIFESPAN MANAGER ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Personal Data Validator API started")
    yield
    logger.info("Personal Data Validator API stopped")


# ==================== FASTAPI INITIALIZATION ====================
app = FastAPI(
    title="Personal Data Validator API",
    description="REST API to validate and normalize personal data using Pydantic",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Soporte",
        "url": "http://localhost:8000"
    }
)


# ==================== ROUTES ====================

@app.get("/", tags=["Info"])
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "name": "Personal Data Validator API",
        "version": "1.0.0",
        "description": "Personal data validation REST API",
        "documentation": "http://localhost:8000/docs",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        API health status
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/validate", tags=["Validation"])
async def validate_user(usuario: UsuarioValidation) -> Dict[str, Any]:
    """Validate a user's personal data.

    Required fields:
        - first_name (string, minimum 2 characters)
        - last_name (string, minimum 2 characters)
        - email (string, valid email format)

    Optional fields:
        - phone (string, digits only, minimum 7 digits)
        - age (int, between 0 and 120)
    """
    try:
        # Log the request
        logger.info(
            f"POST /validate - Email: {usuario.email}, "
            f"First: {usuario.first_name}, Last: {usuario.last_name}"
        )

        # Prepare successful response
        response = {
            "valid": True,
            "message": "Data validated successfully",
            "data": {
                "first_name": usuario.first_name,
                "last_name": usuario.last_name,
                "email": usuario.email,
                "phone": usuario.phone,
                "age": usuario.age
            },
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"Validation successful for: {usuario.email}")
        return response
        
    except ValidationError as e:
        errors_formatted = format_validation_errors(e.errors())

        logger.warning(f"Validation error: {json.dumps(errors_formatted)}")

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "valid": False,
                "message": "Provided data contains validation errors",
                "errors": errors_formatted,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in /validate: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "valid": False,
                "message": "Internal server error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


# ==================== MANEJADOR DE EXCEPCIONES ====================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    logger.error(f"HTTP Error {exc.status_code} on {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler for unhandled exceptions."""
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "valid": False,
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )


# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )
