# API Validadora de Datos Personales

API REST funcional construida con **FastAPI** y **Python 3.12** para validar datos personales de usuarios con validaciones avanzadas, manejo de errores global, y documentación automática mediante Swagger UI.

## 🚀 Características

✅ **Validación robusta** con Pydantic  
✅ **Normalización automática** de nombres y apellidos  
✅ **Validación de email** con regex  
✅ **Validación de teléfono** (numérico, mínimo 7 dígitos)  
✅ **Rango de edad** (0-120 años)  
✅ **Swagger UI** automático para probar la API  
✅ **Logging completo** para cada petición  
✅ **Manejo de errores global** con mensajes claros  
✅ **Código modular y escalable**  
✅ **100% funcional y listo para producción**

---

## 📋 Requisitos

- Python 3.11+
- pip o conda

---

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd /home/pantuflitos/Proyectos/API_Validadora
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecutar la API

### Opción 1: Con uvicorn (recomendado)

```bash
python -m uvicorn main:app --host localhost --port 8000
```

### Opción 2: Ejecutar directamente

```bash
python main.py
```

La API estará disponible en: **http://localhost:8000**

---

## 📚 Documentación de la API

### Endpoints disponibles

#### 1. **GET /** - Información de la API

```http
GET http://localhost:8000/
```

**Respuesta exitosa (200):**
```json
{
  "nombre": "API Validadora",
  "version": "1.0.0",
  "descripcion": "API REST para validar datos personales de usuarios",
  "documentacion": "http://localhost:8000/docs",
  "timestamp": "2025-12-11T22:50:31.132924"
}
```

#### 2. **GET /health** - Health Check

```http
GET http://localhost:8000/health
```

**Respuesta exitosa (200):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-11T22:50:31.134761"
}
```

#### 3. **POST /validar** - Validar datos personales

```http
POST http://localhost:8000/validar
Content-Type: application/json
```

**Esquema de entrada:**

| Campo | Tipo | Requerido | Validación |
|-------|------|-----------|-----------|
| `nombre` | string | ✅ Sí | Mínimo 2 caracteres |
| `apellido` | string | ✅ Sí | Mínimo 2 caracteres |
| `email` | string | ✅ Sí | Formato email válido |
| `telefono` | string | ❌ No | Numérico, mínimo 7 dígitos |
| `edad` | int | ❌ No | Rango 0-120 |

**Ejemplo de petición:**

```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan.perez@example.com",
    "telefono": "1234567",
    "edad": 30
  }'
```

**Respuesta exitosa (200):**

```json
{
  "valido": true,
  "mensaje": "Datos validados correctamente",
  "datos": {
    "nombre": "Juan",
    "apellido": "Perez",
    "email": "juan.perez@example.com",
    "telefono": "1234567",
    "edad": 30
  },
  "timestamp": "2025-12-11T22:50:31.141245"
}
```

**Ejemplo con error de validación (422):**

```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "a",
    "apellido": "perez",
    "email": "email-inválido"
  }'
```

**Respuesta con error (422):**

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "nombre"],
      "msg": "Value error, Debe tener mínimo 2 caracteres",
      "input": "a"
    },
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
      "input": "email-inválido"
    }
  ]
}
```

---

## 🧪 Pruebas

### Ejecutar script de pruebas automatizadas

```bash
python test_api.py
```

Este script ejecuta 11 pruebas diferentes que incluyen:

✅ Endpoint raíz  
✅ Health check  
✅ Validación exitosa  
✅ Validación sin campos opcionales  
✅ Error: Nombre muy corto  
✅ Error: Email inválido  
✅ Error: Teléfono muy corto  
✅ Error: Teléfono no numérico  
✅ Error: Edad fuera de rango  
✅ Error: Campos obligatorios faltantes  
✅ Normalización de nombres  

**Salida esperada:**
```
============================================================
PRUEBAS DE LA API VALIDADORA
============================================================
✓ API disponible en http://localhost:8000
...
Pruebas exitosas: 11/11
============================================================

¡Todas las pruebas pasaron correctamente!
```

---

## 🧩 Estructura del Proyecto

```
API_Validadora/
├── main.py                 # Aplicación principal (FastAPI)
├── app/
│   ├── __init__.py        # Inicializador del paquete
│   ├── models.py          # Modelos Pydantic con validadores
│   └── validators.py      # Funciones de validación personalizadas
├── test_api.py            # Script de pruebas automatizadas
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

---

## 📦 Dependencias

| Paquete | Versión | Propósito |
|---------|---------|----------|
| `fastapi` | 0.104.1 | Framework web moderno |
| `pydantic` | 2.5.0 | Validación de datos |
| `pydantic-extra-types` | 2.1.0 | Tipos adicionales de Pydantic |
| `uvicorn[standard]` | 0.24.0 | Servidor ASGI |
| `email-validator` | 2.1.0 | Validación de emails |
| `python-multipart` | 0.0.6 | Parseo de multipart/form-data |
| `requests` | (en test_api.py) | Cliente HTTP para pruebas |

---

## 🔍 Swagger UI (Documentación Interactiva)

Accede a la documentación interactiva y prueba los endpoints en tiempo real:

**URL:** http://localhost:8000/docs

En Swagger UI puedes:
- Ver todos los endpoints disponibles
- Probar las peticiones en tiempo real
- Ver esquemas JSON automáticos
- Visualizar ejemplos de respuestas

---

## 📊 Validaciones Implementadas

### Nombres y Apellidos
- ✅ Mínimo 2 caracteres
- ✅ Se capitalizan automáticamente (primera letra mayúscula, resto minúsculas)
- ✅ Se eliminan espacios en blanco innecesarios

### Email
- ✅ Formato válido según RFC 5322
- ✅ Validación con librería `email-validator`
- ✅ Campo obligatorio

### Teléfono
- ✅ Solo dígitos (0-9)
- ✅ Mínimo 7 dígitos
- ✅ Opcional (puede ser null)
- ✅ Se eliminan espacios en blanco

### Edad
- ✅ Rango 0-120 años
- ✅ Tipo int (entero)
- ✅ Opcional (puede ser null)

---

## 📝 Logging

La API registra automáticamente:
- Hora exacta de cada petición
- Endpoint solicitado
- Datos del usuario validado
- Resultado de la validación
- Errores y excepciones

**Ejemplo de logs:**
```
2025-12-11 22:50:31 - main - INFO - API Validadora iniciada correctamente
2025-12-11 22:50:31 - main - INFO - Petición POST /validar - Email: juan.perez@example.com, Nombre: juan, Apellido: perez
2025-12-11 22:50:31 - main - INFO - Validación exitosa para: juan.perez@example.com
```

---

## 🚀 Ejemplo de Uso Completo

### 1. Iniciar la API
```bash
python -m uvicorn main:app --host localhost --port 8000
```

### 2. Hacer una petición desde otro terminal o usando Postman

```bash
curl -X POST http://localhost:8000/validar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "carlos",
    "apellido": "martinez",
    "email": "carlos.martinez@gmail.com",
    "telefono": "1234567890",
    "edad": 25
  }' | python -m json.tool
```

### 3. Respuesta esperada

```json
{
  "valido": true,
  "mensaje": "Datos validados correctamente",
  "datos": {
    "nombre": "Carlos",
    "apellido": "Martinez",
    "email": "carlos.martinez@gmail.com",
    "telefono": "1234567890",
    "edad": 25
  },
  "timestamp": "2025-12-11T22:50:31.141245"
}
```

---

## 🛠️ Personalización

### Cambiar puerto
```bash
python -m uvicorn main:app --host localhost --port 9000
```

### Cambiar host
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Modo desarrollo con auto-reload
```bash
python -m uvicorn main:app --host localhost --port 8000 --reload
```

---

## 📈 Escalabilidad

Este proyecto está diseñado para ser escalable:

- ✅ Estructura modular con separación de concerns
- ✅ Validadores reutilizables
- ✅ Manejadores de errores globales
- ✅ Logging centralizado
- ✅ Fácil de añadir nuevos endpoints
- ✅ Compatible con bases de datos (SQLAlchemy, etc.)
- ✅ Compatible con autenticación (JWT, OAuth2, etc.)

---

## 🐛 Resolución de Problemas

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Solución:** Asegúrate de instalar las dependencias: `pip install -r requirements.txt`

### Error: "Address already in use: ('localhost', 8000)"
**Solución:** El puerto 8000 ya está en uso. Usa otro puerto:
```bash
python -m uvicorn main:app --host localhost --port 8001
```

### Las validaciones no funcionan
**Solución:** Verifica que estés enviando los datos en formato JSON con el header `Content-Type: application/json`

---

## 📜 Licencia

Proyecto libre para uso educativo y profesional.

---

## 👨‍💻 Autor

Proyecto de API REST con FastAPI - Diciembre 2025

---

## 📞 Soporte

Para problemas o preguntas, revisa:
1. La documentación en Swagger: http://localhost:8000/docs
2. Este README
3. Los comentarios en el código

---

## ✨ Checklist de Implementación

- ✅ API REST funcional con FastAPI
- ✅ Endpoints POST /validar, GET /, GET /health
- ✅ Validación con Pydantic
- ✅ Normalización de nombres
- ✅ Validación de email con regex
- ✅ Validación de teléfono (numérico, 7+ dígitos)
- ✅ Validación de edad (0-120)
- ✅ Campos obligatorios: nombre, apellido, email
- ✅ Campos opcionales: teléfono, edad
- ✅ Manejo global de errores
- ✅ Logging por cada petición
- ✅ Swagger UI automático
- ✅ Código modular y limpio
- ✅ requirements.txt completo
- ✅ Script de pruebas automatizadas (11/11 ✅)
- ✅ Servir en localhost:8000 con uvicorn
- ✅ 100% funcional y lista para producción

¡La API está lista para usar! 🎉
