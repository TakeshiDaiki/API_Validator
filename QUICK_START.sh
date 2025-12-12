#!/bin/bash

# QUICK START - API Validadora de Datos Personales
# ================================================

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       API VALIDADORA - INSTRUCCIONES RÁPIDAS (QUICK START)     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "📂 Ubicación del proyecto:"
echo "   /home/pantuflitos/Proyectos/API_Validadora"
echo ""

echo "🚀 PASO 1: Acceder al directorio"
echo "   cd /home/pantuflitos/Proyectos/API_Validadora"
echo ""

echo "⚙️  PASO 2: Activar el entorno virtual (si lo necesitas)"
echo "   source .venv/bin/activate"
echo ""

echo "▶️  PASO 3: Iniciar la API"
echo "   python -m uvicorn main:app --host localhost --port 8000"
echo ""

echo "🌐 PASO 4: Acceder a la API"
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo "   Health: http://localhost:8000/health"
echo ""

echo "📝 PASO 5: Ejemplo de petición con cURL"
echo '   curl -X POST http://localhost:8000/validar \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '\''{
echo '       "nombre": "juan",
echo '       "apellido": "perez",
echo '       "email": "juan@example.com"
echo '     }'\'''
echo ""

echo "🧪 PASO 6: Ejecutar pruebas (en otra terminal)"
echo "   python test_api.py"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📖 Documentación completa en: README.md"
echo "💡 Ejemplos adicionales en: EJEMPLOS.md"
echo ""
echo "✅ La API está 100% funcional y lista para usar."
echo ""
