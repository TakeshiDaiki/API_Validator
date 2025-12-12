"""
Script de prueba para la API Validadora.
Realiza peticiones de ejemplo a los diferentes endpoints.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

# Colores para la salida
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_resultado(titulo: str, response: requests.Response):
    """Imprime el resultado de una petición de forma formateada."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{titulo}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_endpoint_root():
    """Prueba el endpoint raíz."""
    print(f"\n{YELLOW}Probando endpoint raíz...{RESET}")
    response = requests.get(f"{BASE_URL}/")
    print_resultado("GET /", response)
    return response.status_code == 200


def test_health_check():
    """Prueba el health check."""
    print(f"\n{YELLOW}Probando health check...{RESET}")
    response = requests.get(f"{BASE_URL}/health")
    print_resultado("GET /health", response)
    return response.status_code == 200


def test_validacion_exitosa():
    """Prueba una validación exitosa."""
    print(f"\n{YELLOW}Probando validación exitosa...{RESET}")
    
    datos = {
        "nombre": "juan",
        "apellido": "perez",
        "email": "juan.perez@example.com",
        "telefono": "1234567",
        "edad": 30
    }
    
    response = requests.post(
        f"{BASE_URL}/validar",
        json=datos,
        headers={"Content-Type": "application/json"}
    )
    print_resultado("POST /validar - Validación Exitosa", response)
    return response.status_code == 200


def test_validacion_sin_telefono_edad():
    """Prueba validación sin campos opcionales."""
    print(f"\n{YELLOW}Probando validación sin teléfono y edad...{RESET}")
    
    datos = {
        "nombre": "maria",
        "apellido": "garcia",
        "email": "maria.garcia@example.com"
    }
    
    response = requests.post(
        f"{BASE_URL}/validar",
        json=datos
    )
    print_resultado("POST /validar - Sin teléfono y edad", response)
    return response.status_code == 200


def test_nombre_muy_corto():
    """Prueba error: nombre muy corto."""
    print(f"\n{YELLOW}Probando error: nombre muy corto...{RESET}")
    
    datos = {
        "nombre": "a",
        "apellido": "perez",
        "email": "test@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Nombre muy corto", response)
    return response.status_code == 422


def test_email_inválido():
    """Prueba error: email inválido."""
    print(f"\n{YELLOW}Probando error: email inválido...{RESET}")
    
    datos = {
        "nombre": "juan",
        "apellido": "perez",
        "email": "email-inválido"
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Email inválido", response)
    return response.status_code == 422


def test_telefono_muy_corto():
    """Prueba error: teléfono muy corto."""
    print(f"\n{YELLOW}Probando error: teléfono muy corto...{RESET}")
    
    datos = {
        "nombre": "juan",
        "apellido": "perez",
        "email": "juan@example.com",
        "telefono": "123"
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Teléfono muy corto", response)
    return response.status_code == 422


def test_telefono_no_numerico():
    """Prueba error: teléfono no numérico."""
    print(f"\n{YELLOW}Probando error: teléfono no numérico...{RESET}")
    
    datos = {
        "nombre": "juan",
        "apellido": "perez",
        "email": "juan@example.com",
        "telefono": "123-456-7890"
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Teléfono no numérico", response)
    return response.status_code == 422


def test_edad_fuera_rango():
    """Prueba error: edad fuera de rango."""
    print(f"\n{YELLOW}Probando error: edad fuera de rango...{RESET}")
    
    datos = {
        "nombre": "juan",
        "apellido": "perez",
        "email": "juan@example.com",
        "edad": 150
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Edad fuera de rango", response)
    return response.status_code == 422


def test_campos_obligatorios_faltantes():
    """Prueba error: campos obligatorios faltantes."""
    print(f"\n{YELLOW}Probando error: campos obligatorios faltantes...{RESET}")
    
    datos = {
        "nombre": "juan"
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Campos obligatorios faltantes", response)
    return response.status_code == 422


def test_normalizacion_nombres():
    """Prueba normalización de nombres."""
    print(f"\n{YELLOW}Probando normalización de nombres...{RESET}")
    
    datos = {
        "nombre": "jUaN",
        "apellido": "pEReZ",
        "email": "test@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/validar", json=datos)
    print_resultado("POST /validar - Normalización de nombres", response)
    
    if response.status_code == 200:
        data = response.json()
        nombre = data.get('datos', {}).get('nombre')
        apellido = data.get('datos', {}).get('apellido')
        
        if nombre == "Juan" and apellido == "Perez":
            print(f"{GREEN}✓ Normalización correcta: {nombre} {apellido}{RESET}")
            return True
        else:
            print(f"{RED}✗ Normalización fallida: {nombre} {apellido}{RESET}")
            return False
    
    return False


def main():
    """Ejecuta todas las pruebas."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}PRUEBAS DE LA API VALIDADORA{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Esperar a que la API esté disponible
    import time
    max_intentos = 5
    for intento in range(max_intentos):
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            print(f"{GREEN}✓ API disponible en {BASE_URL}{RESET}")
            break
        except requests.exceptions.ConnectionError:
            if intento < max_intentos - 1:
                print(f"{YELLOW}Esperando a que la API esté disponible... ({intento + 1}/{max_intentos}){RESET}")
                time.sleep(1)
            else:
                print(f"{RED}✗ No se pudo conectar a la API{RESET}")
                return
    
    # Lista de pruebas
    pruebas = [
        ("Endpoint raíz", test_endpoint_root),
        ("Health check", test_health_check),
        ("Validación exitosa", test_validacion_exitosa),
        ("Validación sin campos opcionales", test_validacion_sin_telefono_edad),
        ("Error: Nombre muy corto", test_nombre_muy_corto),
        ("Error: Email inválido", test_email_inválido),
        ("Error: Teléfono muy corto", test_telefono_muy_corto),
        ("Error: Teléfono no numérico", test_telefono_no_numerico),
        ("Error: Edad fuera de rango", test_edad_fuera_rango),
        ("Error: Campos obligatorios faltantes", test_campos_obligatorios_faltantes),
        ("Normalización de nombres", test_normalizacion_nombres),
    ]
    
    resultados = []
    for nombre, test in pruebas:
        try:
            resultado = test()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"{RED}✗ Error en prueba {nombre}: {str(e)}{RESET}")
            resultados.append((nombre, False))
    
    # Resumen de resultados
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}RESUMEN DE RESULTADOS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    exitosas = sum(1 for _, resultado in resultados if resultado)
    totales = len(resultados)
    
    for nombre, resultado in resultados:
        simbolo = f"{GREEN}✓{RESET}" if resultado else f"{RED}✗{RESET}"
        print(f"{simbolo} {nombre}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"Pruebas exitosas: {GREEN}{exitosas}/{totales}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    if exitosas == totales:
        print(f"\n{GREEN}¡Todas las pruebas pasaron correctamente!{RESET}")
    else:
        print(f"\n{YELLOW}Algunas pruebas fallaron. Revisa los errores arriba.{RESET}")


if __name__ == "__main__":
    main()
