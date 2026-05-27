# Script de prueba rapida del bot

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  PRUEBA RAPIDA DEL BOT - API FINANCIERA" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

Set-Location $PSScriptRoot

# Verificar .env
if (-not (Test-Path ".env")) {
    Write-Host "`n[X] ERROR: No se encuentra .env" -ForegroundColor Red
    exit
}

Write-Host "`n[OK] Archivo .env encontrado" -ForegroundColor Green

# Leer token del .env
$envContent = Get-Content .env | Where-Object { $_ -match "TELEGRAM_BOT_TOKEN=" }
if ($envContent -match "TELEGRAM_BOT_TOKEN=(.+)") {
    $token = $matches[1].Trim()
    if ($token -eq "TU_TOKEN_AQUI" -or $token -eq "") {
        Write-Host "[X] El token no esta configurado en .env" -ForegroundColor Red
        exit
    }
    Write-Host "[OK] Token configurado correctamente" -ForegroundColor Green
    Write-Host "     Bot: @API_PF_VIU_bot" -ForegroundColor Gray
}

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "`n[X] Python no esta instalado" -ForegroundColor Red
    exit
}

# Verificar/instalar dependencias
Write-Host "`n[...] Verificando dependencias..." -ForegroundColor Cyan

$needsInstall = $false
python -c "import telegram" 2>$null
if ($LASTEXITCODE -ne 0) { $needsInstall = $true }

if ($needsInstall) {
    Write-Host "[...] Instalando dependencias..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Dependencias instaladas" -ForegroundColor Green
    } else {
        Write-Host "[X] Error al instalar dependencias" -ForegroundColor Red
        exit
    }
} else {
    Write-Host "[OK] Dependencias instaladas" -ForegroundColor Green
}

# Instrucciones finales
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "  SIGUIENTE PASO" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

Write-Host "`n[SEGURIDAD] Configurar usuarios autorizados (Recomendado):" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. Abre Telegram y busca: " -NoNewline -ForegroundColor White
Write-Host "@userinfobot" -ForegroundColor Cyan
Write-Host "   2. Envia: " -NoNewline -ForegroundColor White
Write-Host "/start" -ForegroundColor Cyan
Write-Host "   3. Copia tu ID (ejemplo: 123456789)" -ForegroundColor White
Write-Host "   4. Edita " -NoNewline -ForegroundColor White
Write-Host ".env" -NoNewline -ForegroundColor Cyan
Write-Host " y anade tu ID en AUTHORIZED_USERS" -ForegroundColor White
Write-Host ""
Write-Host "   Si no configuras esto, " -NoNewline -ForegroundColor Gray
Write-Host "cualquiera podra usar tu bot" -ForegroundColor Red
Write-Host ""

Write-Host "`n[INICIAR] Opciones para iniciar el bot:" -ForegroundColor Green
Write-Host ""
Write-Host "   Opcion 1 - Script automatico:" -ForegroundColor White
Write-Host "   " -NoNewline
Write-Host ".\start_bot.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Opcion 2 - Manualmente:" -ForegroundColor White
Write-Host "   " -NoNewline
Write-Host "python bot.py" -ForegroundColor Cyan
Write-Host ""

Write-Host "==================================================" -ForegroundColor Cyan

Write-Host "`nDeseas iniciar el bot ahora? (S/N): " -NoNewline -ForegroundColor Yellow
$respuesta = Read-Host

if ($respuesta -eq "S" -or $respuesta -eq "s" -or $respuesta -eq "Y" -or $respuesta -eq "y") {
    Write-Host "`n[INICIANDO] Bot iniciando..." -ForegroundColor Green
    Write-Host "Presiona Ctrl+C para detener`n" -ForegroundColor Gray
    python bot.py
} else {
    Write-Host "`n[OK] Configuracion completa. Ejecuta " -NoNewline -ForegroundColor Green
    Write-Host ".\start_bot.ps1" -NoNewline -ForegroundColor Cyan
    Write-Host " cuando estes listo." -ForegroundColor Green
}
