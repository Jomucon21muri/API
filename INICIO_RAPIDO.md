# Inicio rápido

## Ejecutar el sistema completo en 30 segundos

### Linux/Mac:
```bash
./start.sh
```

### Windows PowerShell:
```powershell
.\start_dashboard.ps1
```

### Manual (dos terminales):

**Terminal 1 - API:**
```bash
cd api
python3 app.py
```

**Terminal 2 - Dashboard:**
```bash
python3 -m http.server 8080
```

## Acceder al sistema

1. **Dashboard**: http://localhost:8080
2. **API**: http://localhost:5000/api/health

## Configuración del dashboard

En la sección "Settings":
- **URL de API**: http://localhost:5000/api
- **API Key**: api_key_demo_12345

Hacer clic en "Test Connection" para verificar.

## Datos de prueba

El sistema incluye:
- 40 clientes en 11 países
- 368 transacciones
- 160 posiciones de portfolio
- 15 acciones del mercado

## Problemas comunes

### "Failed to fetch" al probar conexión:

1. Verificar que la API esté corriendo:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. Acceder al dashboard desde http://localhost:8080 (no abrir archivo directamente)

3. Verificar configuración en Settings

Ver más en [README.md](README.md) sección "Solución de problemas"
