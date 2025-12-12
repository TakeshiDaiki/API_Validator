#!/bin/bash

# Script de inicio rápido para la API Validadora

echo "============================================================"
echo "🚀 API Validadora de Datos Personales"
echo "============================================================"
echo ""

# Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado"
    exit 1
fi

echo "✓ Python encontrado: $(python --version)"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -q -r requirements.txt

echo ""
echo "============================================================"
echo "✅ Configuración completada"
echo "============================================================"
echo ""
echo "📊 Opciones disponibles:"
echo ""
echo "1️⃣  Iniciar servidor:      python -m uvicorn main:app --host localhost --port 8000"
echo "2️⃣  Ejecutar pruebas:      python test_api.py"
echo "3️⃣  Acceder a Swagger:     http://localhost:8000/docs"
echo ""
echo "============================================================"
