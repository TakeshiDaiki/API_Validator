# API Validadora de Datos Personales

API REST con FastAPI para validar y normalizar datos personales usando Pydantic.

Características
- Validación y normalización de `first_name` y `last_name` (nombres y apellidos)
- Validación de `email` con un validador robusto
- Campos opcionales: `phone` (solo dígitos, mínimo 7) y `age` (0-120)
- Capitalización automática de nombres
- Documentación Swagger UI y ReDoc
- Logging y manejo global de errores

Inicio rápido
1. Crear y activar un entorno virtual (recomendado):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la app localmente:

```bash
uvicorn main:app --host localhost --port 8000
```

4. Abrir Swagger UI: http://localhost:8000/docs

Endpoints
- `GET /` — Información y metadatos de la API
- `GET /health` — Health check
- `POST /validate` — Validar datos personales (cuerpo JSON)

Ejemplo de petición

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"juan","last_name":"perez","email":"juan@example.com","phone":"1234567","age":30}'
```

Ejemplo de respuesta

```json
{
  "valid": true,
  "message": "Data validated successfully",
  "data": {
    "first_name": "Juan",
    "last_name": "Perez",
    "email": "juan@example.com",
    "phone": "1234567",
    "age": 30
  },
  "timestamp": "2025-12-11T22:56:11.327998"
}
```

Pruebas

Ejecutar el script de pruebas automatizadas:

```bash
python test_api.py
```

Licencia

Proyecto con licencia MIT — ver el archivo `LICENSE`.

Contribuciones

Se aceptan contribuciones; abre un issue o un pull request en GitHub.
