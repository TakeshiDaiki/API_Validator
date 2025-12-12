# 📋 Comandos Útiles

## 🚀 Operaciones Básicas

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Iniciar el servidor
```bash
python -m uvicorn main:app --host localhost --port 8000
```

### Iniciar con recarga automática (desarrollo)
```bash
python -m uvicorn main:app --host localhost --port 8000 --reload
```

### Ejecutar pruebas
```bash
python test_api.py
```

---

## 🧪 Pruebas con curl

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Info de la API
```bash
curl http://localhost:8000/
```

### 3. Validación exitosa (todos los campos)
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan@example.com",
    "telefono": "1234567890",
    "edad": 30
  }'
```

### 4. Validación con solo campos obligatorios
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "maria",
    "apellido": "garcia",
    "email": "maria@example.com"
  }'
```

### 5. Prueba de error (nombre muy corto)
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "a",
    "apellido": "perez",
    "email": "test@example.com"
  }'
```

### 6. Prueba de error (email inválido)
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan",
    "apellido": "perez",
    "email": "email-invalido"
  }'
```

### 7. Prueba de error (teléfono muy corto)
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan@example.com",
    "telefono": "123"
  }'
```

### 8. Prueba de error (edad fuera de rango)
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "juan",
    "apellido": "perez",
    "email": "juan@example.com",
    "edad": 150
  }'
```

---

## 🐍 Pruebas con Python

### Script de prueba simple
```python
import requests

url = "http://localhost:8000/validar"

# Datos válidos
datos = {
    "nombre": "carlos",
    "apellido": "lopez",
    "email": "carlos@example.com",
    "edad": 25
}

response = requests.post(url, json=datos)
print(response.json())
```

### Prueba con validaciones
```python
import requests

def validar_usuario(nombre, apellido, email, telefono=None, edad=None):
    url = "http://localhost:8000/validar"
    
    datos = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }
    
    if telefono:
        datos["telefono"] = telefono
    if edad:
        datos["edad"] = edad
    
    response = requests.post(url, json=datos)
    
    if response.status_code == 200:
        print("✅ Validación exitosa")
        print(response.json()["datos"])
    else:
        print("❌ Error de validación")
        print(response.json())

# Probar
validar_usuario("juan", "perez", "juan@example.com", "1234567890", 30)
```

---

## 🌐 Pruebas con JavaScript

### Fetch API
```javascript
const validar = async (nombre, apellido, email, telefono, edad) => {
  const datos = { nombre, apellido, email };
  
  if (telefono) datos.telefono = telefono;
  if (edad) datos.edad = edad;
  
  const response = await fetch('http://localhost:8000/validar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  
  const resultado = await response.json();
  console.log(resultado);
};

// Usar
validar('juan', 'perez', 'juan@example.com', '1234567890', 30);
```

### Axios
```javascript
const axios = require('axios');

axios.post('http://localhost:8000/validar', {
  nombre: 'juan',
  apellido: 'perez',
  email: 'juan@example.com',
  telefono: '1234567890',
  edad: 30
})
.then(res => console.log(res.data))
.catch(err => console.log(err.response.data));
```

---

## 📊 Otras Herramientas

### Con wget
```bash
wget --post-data='{"nombre":"juan","apellido":"perez","email":"juan@example.com"}' \
     --header='Content-Type: application/json' \
     http://localhost:8000/validar -O -
```

### Con Postman
1. Nuevo Request → POST
2. URL: `http://localhost:8000/validar`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "nombre": "juan",
  "apellido": "perez",
  "email": "juan@example.com"
}
```
5. Click en "Send"

### Con httpie (más legible que curl)
```bash
http POST localhost:8000/validar \
  nombre=juan \
  apellido=perez \
  email=juan@example.com
```

---

## 🔍 Verificación y Debugging

### Ver logs del servidor
```bash
# El servidor muestra los logs en la terminal donde se ejecutó
# Busca líneas como:
# INFO:     Petición POST /validar - Email: ...
# INFO:     Validación exitosa para: ...
```

### Verificar que el servidor está activo
```bash
curl -I http://localhost:8000/health
```

### Ver todos los procesos Python
```bash
ps aux | grep python
```

### Detener el servidor
```bash
# En la terminal donde corre el servidor:
# Presiona Ctrl+C
```

---

## 📈 Monitoreo

### Contar peticiones exitosas
```bash
# Ver los logs del servidor y contar líneas con "Validación exitosa"
# En tiempo real:
tail -f logs.txt | grep "Validación exitosa"
```

### Ver estadísticas de peticiones
```bash
# En los logs buscar:
grep "Petición POST" server_logs.txt | wc -l
```

---

## 🚨 Troubleshooting

### Error: "Connection refused"
```bash
# El servidor no está corriendo
# Solución: Inicia el servidor
python -m uvicorn main:app --host localhost --port 8000
```

### Error: "ModuleNotFoundError"
```bash
# Las dependencias no están instaladas
# Solución:
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
# Otro proceso está usando el puerto
# Solución 1: Usa otro puerto
python -m uvicorn main:app --host localhost --port 8001

# Solución 2: Detén el proceso anterior
# Busca el PID y detén: kill -9 <PID>
```

---

## 💡 Tips Útiles

### Guardar respuestas en archivo
```bash
curl -X POST "http://localhost:8000/validar" \
  -H "Content-Type: application/json" \
  -d '{...}' > respuesta.json
```

### Probar múltiples usuarios
```bash
for i in {1..5}; do
  curl -X POST "http://localhost:8000/validar" \
    -H "Content-Type: application/json" \
    -d "{\"nombre\":\"usuario$i\",\"apellido\":\"test\",\"email\":\"user$i@example.com\"}"
  echo ""
done
```

### Medir tiempo de respuesta
```bash
curl -w "\nTiempo: %{time_total}s\n" http://localhost:8000/health
```

---

¡Estos comandos te ayudarán a probar y verificar la API completamente! 🚀
