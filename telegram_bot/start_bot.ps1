# Script para iniciar el bot de Telegram

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 49) -ForegroundColor Cyan
Write-Host "  BOT DE TELEGRAM - API FINANCIERA" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 49) -ForegroundColor Cyan

# Ir al directorio del bot
Set-Location $PSScriptRoot

# Verificar que existe el archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "`n❌ ERROR: No se encuentra el archivo .env" -ForegroundColor Red
    Write-Host "`nPrimeros pasos:" -ForegroundColor Yellow
    Write-Host "1. Copia el archivo .env.example a .env" -ForegroundColor White
    Write-Host "2. Edita .env y añade tu token de Telegram" -ForegroundColor White
    Write-Host "3. Obtén el token de @BotFather en Telegram" -ForegroundColor White
    Write-Host "`nEjemplo de comando:" -ForegroundColor Cyan
    Write-Host "   Copy-Item .env.example .env" -ForegroundColor Gray
    pause
    exit
}

# Verificar que Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "`n✅ Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "`n❌ ERROR: Python no está instalado" -ForegroundColor Red
    pause
    exit
}

# Verificar dependencias
Write-Host "`n📦 Verificando dependencias..." -ForegroundColor Cyan
$packages = @("telegram", "requests", "dotenv")
$missingPackages = @()

foreach ($package in $packages) {
    python -c "import $package" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "⚠️  Faltan algunas dependencias. Instalando..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Error al instalar dependencias" -ForegroundColor Red
        pause
        exit
    }
}

Write-Host "✅ Dependencias OK" -ForegroundColor Green

# Iniciar el bot
Write-Host "`n🤖 Iniciando bot..." -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el bot`n" -ForegroundColor Gray
python bot.py
