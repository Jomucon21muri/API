# Script para iniciar la API y el dashboard automáticamente
# Automatización de procesos financieros

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Dashboard financiero - inicio automático" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Variables de configuración
$API_DIR = Join-Path $PSScriptRoot "api"
$DASHBOARD_FILE = Join-Path $PSScriptRoot "dashboard.html"
$API_URL = "http://localhost:5000"
$API_HEALTH = "$API_URL/api/health"

# Función para verificar si la API está corriendo
function Test-APIRunning {
    try {
        $response = Invoke-WebRequest -Uri $API_HEALTH -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

# Función para iniciar la API
function Start-API {
    Write-Host "[1/3] Iniciando API financiera..." -ForegroundColor Yellow
    
    # Verificar si la API ya está corriendo
    if (Test-APIRunning) {
        Write-Host "  [OK] La API ya esta ejecutandose en $API_URL" -ForegroundColor Green
        return $true
    }
    
    # Verificar que existe el directorio de la API
    if (-not (Test-Path $API_DIR)) {
        Write-Host "  [ERROR] No se encuentra el directorio 'api'" -ForegroundColor Red
        return $false
    }
    
    # Cambiar al directorio de la API
    Push-Location $API_DIR
    
    # Verificar que existe app.py
    if (-not (Test-Path "app.py")) {
        Write-Host "  [ERROR] No se encuentra app.py" -ForegroundColor Red
        Pop-Location
        return $false
    }
    
    # Verificar dependencias
    Write-Host "  -> Verificando dependencias..." -ForegroundColor Gray
    $requirements = Get-Content "requirements.txt" -ErrorAction SilentlyContinue
    if ($requirements) {
        pip install -r requirements.txt --quiet 2>&1 | Out-Null
    }
    
    # Inicializar base de datos si no existe
    if (-not (Test-Path "financial.db")) {
        Write-Host "  -> Inicializando base de datos..." -ForegroundColor Gray
        python -c "from app import db; db.create_all()" 2>&1 | Out-Null
    }
    
    # Iniciar la API en segundo plano
    Write-Host "  -> Lanzando servidor Flask..." -ForegroundColor Gray
    Start-Process python -ArgumentList "app.py" -WindowStyle Hidden -PassThru | Out-Null
    
    Pop-Location
    
    # Esperar a que la API este lista
    Write-Host "  -> Esperando a que la API este disponible..." -ForegroundColor Gray
    $maxAttempts = 10
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 1
        if (Test-APIRunning) {
            Write-Host "  [OK] API iniciada correctamente en $API_URL" -ForegroundColor Green
            return $true
        }
        $attempt++
    }
    
    Write-Host "  [ERROR] La API no respondio despues de $maxAttempts intentos" -ForegroundColor Red
    return $false
}

# Función para abrir el dashboard
function Start-Dashboard {
    Write-Host "[2/3] Abriendo dashboard en el navegador..." -ForegroundColor Yellow
    
    # Verificar que existe el archivo del dashboard
    if (-not (Test-Path $DASHBOARD_FILE)) {
        Write-Host "  [ERROR] No se encuentra dashboard.html" -ForegroundColor Red
        return $false
    }
    
    # Abrir en el navegador predeterminado
    try {
        Start-Process $DASHBOARD_FILE
        Write-Host "  [OK] Dashboard abierto en el navegador" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "  [ERROR] Error al abrir el navegador: $_" -ForegroundColor Red
        Write-Host "  -> Abre manualmente: $DASHBOARD_FILE" -ForegroundColor Yellow
        return $false
    }
}

# Función para mostrar información
function Show-Info {
    Write-Host "[3/3] Información del sistema:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  API URL:       $API_URL" -ForegroundColor White
    Write-Host "  API Health:    $API_HEALTH" -ForegroundColor White
    Write-Host "  Dashboard:     $DASHBOARD_FILE" -ForegroundColor White
    Write-Host "  API Key:       api_key_demo_12345" -ForegroundColor White
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  Sistema iniciado correctamente" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Comandos útiles:" -ForegroundColor White
    Write-Host "  - Ver logs de la API: Get-Process python" -ForegroundColor Gray
    Write-Host "  - Detener la API: Stop-Process -Name python" -ForegroundColor Gray
    Write-Host "  - Probar endpoint: curl $API_HEALTH" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Presiona Ctrl+C para detener este script (la API seguirá ejecutándose)" -ForegroundColor Yellow
}

# Ejecución principal
try {
    # Paso 1: Iniciar API
    $apiStarted = Start-API
    
    if (-not $apiStarted) {
        Write-Host ""
        Write-Host "No se pudo iniciar la API. Verifica los errores anteriores." -ForegroundColor Red
        exit 1
    }
    
    Start-Sleep -Seconds 2
    
    # Paso 2: Abrir Dashboard
    $dashboardOpened = Start-Dashboard
    
    Start-Sleep -Seconds 1
    
    # Paso 3: Mostrar información
    Show-Info
    
    # Mantener el script activo para mostrar logs
    Write-Host "Monitoreando sistema... (Presiona Ctrl+C para salir)" -ForegroundColor Cyan
    Write-Host ""
    
    # Loop infinito para mantener el script activo
    while ($true) {
        Start-Sleep -Seconds 5
        
        # Verificar que la API siga corriendo
        if (-not (Test-APIRunning)) {
            Write-Host "[ALERTA] La API dejó de responder!" -ForegroundColor Red
            break
        }
    }
}
catch {
    Write-Host ""
    Write-Host "Error inesperado: $_" -ForegroundColor Red
    exit 1
}
finally {
    Write-Host ""
    Write-Host "Script finalizado. La API puede seguir ejecutándose en segundo plano." -ForegroundColor Yellow
}
