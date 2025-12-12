"""
API REST para validación de datos personales usando FastAPI.

Endpoints:
    POST /validar - Valida datos personales de un usuario
    GET / - Información de la API
    GET /docs - Documentación interactiva Swagger UI
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.models import UsuarioValidacion

# ==================== CONFIGURACIÓN DE LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== MANEJADOR GLOBAL DE ERRORES ====================
def format_validation_errors(errors: list) -> Dict[str, str]:
    """
    Formatea los errores de validación de Pydantic en un diccionario amigable.
    
    Args:
        errors: Lista de errores de ValidationError de Pydantic
        
    Returns:
        Diccionario con errores por campo
    """
    error_dict = {}
    for error in errors:
        field = error['loc'][0] if error['loc'] else 'general'
        message = error['msg']
        
        # Hacer el mensaje más legible
        if 'at least 2 characters' in message:
            message = 'Debe tener mínimo 2 caracteres'
        elif 'ensure this value is' in message:
            message = error['msg']
        
        error_dict[str(field)] = message
    
    return error_dict


# ==================== LIFESPAN MANAGER ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestor de ciclo de vida de la aplicación."""
    logger.info("API Validadora iniciada correctamente")
    yield
    logger.info("API Validadora desconectada")


# ==================== INICIALIZACIÓN DE FASTAPI ====================
app = FastAPI(
    title="API Validadora de Datos Personales",
    description="API REST para validar datos personales de usuarios con validaciones avanzadas",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Soporte",
        "url": "http://localhost:8000"
    }
)


# ==================== RUTAS ====================

@app.get("/", tags=["Info"])
async def root() -> Dict[str, Any]:
    """
    Endpoint raíz con información de la API.
    
    Returns:
        Diccionario con información de la API
    """
    return {
        "nombre": "API Validadora",
        "version": "1.0.0",
        "descripcion": "API REST para validar datos personales de usuarios",
        "documentacion": "http://localhost:8000/docs",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """
    Endpoint para verificar el estado de la API.
    
    Returns:
        Estado de la API
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/validar", tags=["Validación"])
async def validar_usuario(usuario: UsuarioValidacion) -> Dict[str, Any]:
    """
    Valida los datos personales de un usuario.
    
    Campos requeridos:
        - nombre (string, mínimo 2 caracteres)
        - apellido (string, mínimo 2 caracteres)
        - email (string, formato email válido)
    
    Campos opcionales:
        - telefono (string, numérico, mínimo 7 dígitos)
        - edad (int, entre 0 y 120)
    
    Args:
        usuario: Objeto UsuarioValidacion con los datos a validar
        
    Returns:
        JSON indicando validación exitosa con datos normalizados
        
    Raises:
        HTTPException: Si hay errores de validación
    """
    try:
        # Log de la petición
        logger.info(
            f"Petición POST /validar - Email: {usuario.email}, "
            f"Nombre: {usuario.nombre}, Apellido: {usuario.apellido}"
        )
        
        # Preparar respuesta exitosa
        response = {
            "valido": True,
            "mensaje": "Datos validados correctamente",
            "datos": {
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "telefono": usuario.telefono,
                "edad": usuario.edad
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Validación exitosa para: {usuario.email}")
        return response
        
    except ValidationError as e:
        # Formatea los errores de Pydantic
        errores_formateados = format_validation_errors(e.errors())
        
        logger.warning(f"Error de validación: {json.dumps(errores_formateados)}")
        
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "valido": False,
                "mensaje": "Los datos proporcionados contienen errores de validación",
                "errores": errores_formateados,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except Exception as e:
        logger.error(f"Error inesperado en /validar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "valido": False,
                "mensaje": "Error interno del servidor",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


# ==================== MANEJADOR DE EXCEPCIONES ====================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Manejador global de excepciones HTTP.
    
    Args:
        request: Objeto de la petición
        exc: Excepción HTTP
        
    Returns:
        Respuesta JSON con detalles del error
    """
    logger.error(
        f"Error HTTP {exc.status_code} en {request.method} {request.url.path}: {exc.detail}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Manejador global de excepciones no manejadas.
    
    Args:
        request: Objeto de la petición
        exc: Excepción no manejada
        
    Returns:
        Respuesta JSON con error interno
    """
    logger.error(
        f"Excepción no manejada en {request.method} {request.url.path}: {str(exc)}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "valido": False,
            "mensaje": "Error interno del servidor",
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
