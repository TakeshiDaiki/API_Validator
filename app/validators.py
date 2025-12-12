"""
Funciones de validación personalizada para datos de usuario.
"""

import re
from typing import Tuple, Dict, List


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida el formato de un email usando expresión regular.
    
    Args:
        email: String del email a validar
        
    Returns:
        Tupla con (es_válido, mensaje_error)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    return False, "Formato de email inválido"


def capitalizar_nombre(nombre: str) -> str:
    """
    Capitaliza la primera letra del nombre y minúsculas el resto.
    
    Args:
        nombre: String del nombre a normalizar
        
    Returns:
        Nombre normalizado
    """
    return nombre.strip().capitalize()


def contar_errores_validacion(errores: Dict) -> int:
    """
    Cuenta la cantidad de campos con errores de validación.
    
    Args:
        errores: Diccionario de errores de validación
        
    Returns:
        Cantidad de campos con errores
    """
    return len(errores)
