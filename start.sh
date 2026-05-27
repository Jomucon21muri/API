#!/bin/bash

# Script para iniciar el sistema completo (API + Dashboard)
# Uso: ./start.sh

echo "========================================="
echo "  Iniciando Sistema Dashboard API"
echo "========================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "index.html" ]; then
    echo "Error: Este script debe ejecutarse desde la raíz del proyecto"
    exit 1
fi

# Verificar dependencias de Python
echo "Verificando dependencias de Python..."
cd api
python3 -c "import flask, flask_cors, sqlalchemy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependencias de Python..."
    pip install -q flask flask-cors flask-sqlalchemy python-dotenv
fi
cd ..

# Verificar base de datos
if [ ! -f "api/instance/financial.db" ]; then
    echo "Base de datos no encontrada. Inicializando..."
    python3 scripts/populate_db.py
fi

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "Deteniendo servicios..."
    kill $API_PID 2>/dev/null
    kill $WEB_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar API en segundo plano
echo ""
echo "Iniciando API en puerto 5000..."
cd api
python3 app.py > ../api.log 2>&1 &
API_PID=$!
cd ..

# Esperar a que la API inicie
echo "Esperando a que la API inicie..."
sleep 3

# Verificar que la API esté corriendo
if ! curl -s http://localhost:5000/api/health > /dev/null; then
    echo "Error: La API no pudo iniciarse. Revisa api.log para más detalles."
    cat api.log
    exit 1
fi

echo "API iniciada correctamente"

# Iniciar servidor web para el dashboard
echo ""
echo "Iniciando servidor web en puerto 8080..."
python3 -m http.server 8080 > web.log 2>&1 &
WEB_PID=$!

echo ""
echo "========================================="
echo "  Sistema iniciado correctamente"
echo "========================================="
echo ""
echo "API:       http://localhost:5000/api/health"
echo "Dashboard: http://localhost:8080"
echo ""
echo "Configuración del dashboard:"
echo "  - URL de API: http://localhost:5000/api"
echo "  - API Key: api_key_demo_12345"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Mantener el script corriendo
wait
