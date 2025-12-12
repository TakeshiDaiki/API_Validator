"""
Modelos Pydantic para validación de datos de usuario.
"""

from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo
from typing import Optional
import re


class UsuarioValidacion(BaseModel):
    """Modelo para validación de datos personales del usuario."""
    
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    edad: Optional[int] = None
    
    @field_validator('nombre', 'apellido')
    @classmethod
    def validar_nombres(cls, v: str) -> str:
        """Valida que nombre y apellido tengan mínimo 2 caracteres y normaliza."""
        if not v or len(v.strip()) < 2:
            raise ValueError('Debe tener mínimo 2 caracteres')
        # Normalizar: capitalizar primera letra y minúsculas el resto
        return v.strip().capitalize()
    
    @field_validator('telefono')
    @classmethod
    def validar_telefono(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el teléfono sea numérico y tenga mínimo 7 dígitos."""
        if v is None:
            return v
        
        # Remover espacios en blanco
        v = v.strip()
        
        # Verificar que sea numérico
        if not v.isdigit():
            raise ValueError('El teléfono debe contener solo dígitos')
        
        # Verificar longitud mínima
        if len(v) < 7:
            raise ValueError('El teléfono debe tener mínimo 7 dígitos')
        
        return v
    
    @field_validator('edad')
    @classmethod
    def validar_edad(cls, v: Optional[int]) -> Optional[int]:
        """Valida que la edad esté entre 0 y 120."""
        if v is None:
            return v
        
        if v < 0 or v > 120:
            raise ValueError('La edad debe estar entre 0 y 120 años')
        
        return v
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "nombre": "juan",
                "apellido": "perez",
                "email": "juan.perez@example.com",
                "telefono": "1234567",
                "edad": 30
            }
        }
