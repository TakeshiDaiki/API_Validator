# 🚀 Guía Rápida de Inicio

## ⚡ 30 segundos para tener la API funcionando

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Iniciar el servidor
```bash
python -m uvicorn main:app --host localhost --port 8000
```

### 3️⃣ Abrir documentación interactiva
```
http://localhost:8000/docs
```

---

## 📝 Probar la API

### Con curl (terminal)

**Validación exitosa:**
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"juan","apellido":"perez","email":"juan@example.com"}'
```

**Respuesta:**
```json
{
  "valido": true,
  "mensaje": "Datos validados correctamente",
  "datos": {
    "nombre": "Juan",
    "apellido": "Perez",
    "email": "juan@example.com",
    "telefono": null,
    "edad": null
  }
}
```

### Con Python

```python
import requests

url = "http://localhost:8000/validar"
datos = {
    "nombre": "maria",
    "apellido": "garcia",
    "email": "maria@example.com",
    "telefono": "1234567",
    "edad": 28
}

response = requests.post(url, json=datos)
print(response.json())
```

### Con JavaScript/Fetch

```javascript
const datos = {
  nombre: "carlos",
  apellido: "lopez",
  email: "carlos@example.com"
};

fetch('http://localhost:8000/validar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(datos)
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🧪 Ejecutar pruebas

```bash
python test_api.py
```

Resultado esperado: **11/11 pruebas exitosas ✓**

---

## 📚 Documentación

| Link | Descripción |
|------|------------|
| [README.md](README.md) | Documentación completa |
| [EJEMPLOS.md](EJEMPLOS.md) | Ejemplos en múltiples lenguajes |
| http://localhost:8000/docs | Swagger UI interactivo |
| http://localhost:8000/redoc | Documentación ReDoc |

---

## 🎯 Campos de validación

| Campo | Requerido | Validación |
|-------|-----------|-----------|
| **nombre** | ✅ Sí | Mínimo 2 caracteres |
| **apellido** | ✅ Sí | Mínimo 2 caracteres |
| **email** | ✅ Sí | Formato email válido |
| **telefono** | ❌ No | Solo dígitos, mínimo 7 |
| **edad** | ❌ No | Entre 0 y 120 |

---

## 🚨 Errores comunes

### Error: "Connection refused"
- Asegúrate de que el servidor está corriendo: `python -m uvicorn main:app --host localhost --port 8000`

### Error: "Module not found"
- Instala las dependencias: `pip install -r requirements.txt`

### Error: "Email inválido"
- Verifica que el email tenga el formato correcto: `usuario@dominio.com`

---

## 🎉 ¡Listo!

Tu API REST está completamente funcional y lista para:
- ✅ Probar en local
- ✅ Integrar con tu aplicación
- ✅ Desplegar en producción
- ✅ Escalar según necesites

**¡Diviértete construyendo!** 🚀
