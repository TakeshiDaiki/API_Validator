# Ejemplos de Uso de la API Validadora

## 🔧 Ejemplos con cURL

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Obtener información de la API
```bash
curl http://localhost:8000/
```

### 3. Validación exitosa con todos los campos
```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan.perez@example.com",
    "telefono": "1234567890",
    "edad": 30
  }'
```

### 4. Validación sin campos opcionales
```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "maria",
    "apellido": "garcia",
    "email": "maria.garcia@example.com"
  }'
```

### 5. Error: Email inválido
```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "carlos",
    "apellido": "lopez",
    "email": "email-invalido"
  }'
```

### 6. Guardando respuesta en archivo
```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "ana",
    "apellido": "martinez",
    "email": "ana@example.com"
  }' > respuesta.json
```

### 7. Con formato JSON pretty-printed
```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "luis",
    "apellido": "rodriguez",
    "email": "luis@example.com",
    "edad": 25
  }' | python -m json.tool
```

---

## 🐍 Ejemplos con Python

### 1. Uso básico con requests
```python
import requests
import json

url = "http://localhost:8000/validar"
datos = {
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan.perez@example.com",
    "telefono": "1234567890",
    "edad": 30
}

respuesta = requests.post(url, json=datos)
print(json.dumps(respuesta.json(), indent=2))
```

### 2. Manejo de errores
```python
import requests

url = "http://localhost:8000/validar"
datos = {
    "nombre": "a",  # Muy corto
    "apellido": "perez",
    "email": "juan.perez@example.com"
}

respuesta = requests.post(url, json=datos)

if respuesta.status_code == 200:
    print("✓ Validación exitosa")
    print(respuesta.json())
elif respuesta.status_code == 422:
    print("✗ Error de validación")
    print(respuesta.json())
else:
    print(f"✗ Error del servidor: {respuesta.status_code}")
```

### 3. Validar múltiples usuarios
```python
import requests
import json

usuarios = [
    {
        "nombre": "juan",
        "apellido": "perez",
        "email": "juan@example.com",
        "telefono": "1234567890",
        "edad": 30
    },
    {
        "nombre": "maria",
        "apellido": "garcia",
        "email": "maria@example.com",
        "edad": 25
    },
    {
        "nombre": "carlos",
        "apellido": "lopez",
        "email": "carlos@example.com"
    }
]

url = "http://localhost:8000/validar"

for usuario in usuarios:
    respuesta = requests.post(url, json=usuario)
    
    if respuesta.status_code == 200:
        data = respuesta.json()['datos']
        print(f"✓ {data['nombre']} {data['apellido']} - {data['email']}")
    else:
        print(f"✗ Error validando: {usuario}")
```

### 4. Con client HTTP personalizado
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def crear_sesion_con_reintentos():
    """Crea una sesión con reintentos automáticos"""
    s = requests.Session()
    reintentos = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    adaptador = HTTPAdapter(max_retries=reintentos)
    s.mount('http://', adaptador)
    s.mount('https://', adaptador)
    return s

sesion = crear_sesion_con_reintentos()

datos = {
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan@example.com"
}

respuesta = sesion.post("http://localhost:8000/validar", json=datos)
print(respuesta.json())
```

### 5. Usando httpx (cliente asincrónico)
```python
import httpx
import asyncio
import json

async def validar_usuario():
    async with httpx.AsyncClient() as client:
        datos = {
            "nombre": "juan",
            "apellido": "perez",
            "email": "juan@example.com"
        }
        
        respuesta = await client.post(
            "http://localhost:8000/validar",
            json=datos
        )
        
        print(json.dumps(respuesta.json(), indent=2))

# Ejecutar
asyncio.run(validar_usuario())
```

---

## 🧪 Test Unitario (pytest)

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validacion_exitosa():
    """Prueba que una validación exitosa devuelve 200"""
    respuesta = client.post(
        "/validar",
        json={
            "nombre": "juan",
            "apellido": "perez",
            "email": "juan@example.com"
        }
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["valido"] == True

def test_email_invalido():
    """Prueba que un email inválido devuelve 422"""
    respuesta = client.post(
        "/validar",
        json={
            "nombre": "juan",
            "apellido": "perez",
            "email": "email-invalido"
        }
    )
    assert respuesta.status_code == 422

def test_nombre_muy_corto():
    """Prueba que nombres cortos devuelven 422"""
    respuesta = client.post(
        "/validar",
        json={
            "nombre": "a",
            "apellido": "perez",
            "email": "test@example.com"
        }
    )
    assert respuesta.status_code == 422

def test_normalizacion_nombres():
    """Prueba que los nombres se normalizan correctamente"""
    respuesta = client.post(
        "/validar",
        json={
            "nombre": "jUaN",
            "apellido": "pErEz",
            "email": "test@example.com"
        }
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()["datos"]
    assert datos["nombre"] == "Juan"
    assert datos["apellido"] == "Perez"

# Ejecutar con: pytest
```

---

## 📡 Ejemplo con JavaScript/Fetch

```javascript
// Validación exitosa
const validarUsuario = async () => {
  const datos = {
    nombre: "juan",
    apellido: "perez",
    email: "juan@example.com",
    telefono: "1234567890",
    edad: 30
  };

  try {
    const respuesta = await fetch("http://localhost:8000/validar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    });

    if (respuesta.ok) {
      const resultado = await respuesta.json();
      console.log("✓ Validación exitosa:", resultado);
    } else {
      const error = await respuesta.json();
      console.error("✗ Error de validación:", error);
    }
  } catch (error) {
    console.error("✗ Error de conexión:", error);
  }
};

// Ejecutar
validarUsuario();
```

---

## 🔄 Validar en batch (Python)

```python
import requests
import json
from concurrent.futures import ThreadPoolExecutor

def validar_usuario(usuario):
    """Valida un usuario y devuelve resultado"""
    try:
        respuesta = requests.post(
            "http://localhost:8000/validar",
            json=usuario,
            timeout=5
        )
        return {
            "usuario": usuario["email"],
            "valido": respuesta.status_code == 200,
            "respuesta": respuesta.json()
        }
    except Exception as e:
        return {
            "usuario": usuario["email"],
            "valido": False,
            "error": str(e)
        }

# Lista de usuarios a validar
usuarios = [
    {"nombre": "juan", "apellido": "perez", "email": "juan@example.com"},
    {"nombre": "maria", "apellido": "garcia", "email": "maria@example.com"},
    {"nombre": "carlos", "apellido": "lopez", "email": "carlos@example.com"},
]

# Validar en paralelo
with ThreadPoolExecutor(max_workers=3) as executor:
    resultados = list(executor.map(validar_usuario, usuarios))

# Mostrar resultados
for resultado in resultados:
    estado = "✓" if resultado["valido"] else "✗"
    print(f"{estado} {resultado['usuario']}")
```

---

Estos ejemplos cubren casos de uso comunes y pueden adaptarse según tus necesidades.
