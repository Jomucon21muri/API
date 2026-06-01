# Guía de inicio rápido

## Descripción general

Esta guía proporciona instrucciones concisas para la inicialización y puesta en marcha del sistema de gestión financiera. El tiempo estimado de configuración es inferior a dos minutos.

## Ejecución del sistema completo

### Entorno Linux/macOS

```bash
./start.sh
```

### Entorno Windows con PowerShell

```powershell
.\start_dashboard.ps1
```

### Ejecución manual (dos terminales simultáneas)

Esta opción ofrece mayor control sobre los procesos de servidor.

**Terminal 1 - Servidor de API:**
```bash
cd api
python3 app.py
```

**Terminal 2 - Servidor web para el panel de control:**
```bash
python3 -m http.server 8080
```

## Acceso a los componentes del sistema

Una vez iniciado el sistema, los siguientes servicios estarán disponibles:

1. **Panel de control (Dashboard)**: http://localhost:8080
2. **API REST**: http://localhost:5000
3. **Verificación de estado**: http://localhost:5000/api/health

## Configuración inicial del panel de control

Acceda a la sección de configuración (Settings) e ingrese los siguientes parámetros:

- **URL base de la API**: http://localhost:5000/api
- **Clave de autenticación (API Key)**: api_key_demo_12345

Utilice la función "Test Connection" para validar la conectividad entre componentes.

## Datos de demostración incluidos

El sistema incluye un conjunto de datos de prueba preconfigurado:

- 40 registros de clientes distribuidos en 11 países
- 368 transacciones financieras de múltiples tipologías
- 160 posiciones activas de portafolio
- 15 acciones del mercado con información actualizada

## Resolución de problemas frecuentes

### Error: "Failed to fetch" al verificar conexión

Este error indica problemas de conectividad entre el panel de control y la API. Siga estos pasos de diagnóstico:

**1. Verificar estado del servidor de API:**
```bash
curl http://localhost:5000/api/health
```

La respuesta esperada debe incluir el campo `"status": "ok"`.

**2. Validar método de acceso al panel de control:**

El panel de control debe accederse mediante http://localhost:8080. No abra el archivo index.html directamente en el navegador, ya que esto causará problemas de política de CORS (Cross-Origin Resource Sharing).

**3. Confirmar configuración de parámetros:**

Revise que la configuración en la sección Settings corresponda exactamente con los valores indicados en la sección de configuración inicial.

**4. Verificar puertos de red:**

Asegúrese de que los puertos 5000 y 8080 no estén siendo utilizados por otros servicios. Para verificar:

```bash
# Linux/macOS
lsof -i :5000
lsof -i :8080

# Windows PowerShell
netstat -ano | findstr :5000
netstat -ano | findstr :8080
```

### Error: "ModuleNotFoundError" al iniciar la API

Este error indica que las dependencias de Python no están instaladas. Ejecute:

```bash
cd api
pip install -r requirements.txt
```

### El panel de control no carga correctamente

Verifique que está utilizando un navegador web moderno (Chrome, Firefox, Safari o Edge en sus versiones actuales).

## Siguientes pasos

Para información detallada sobre arquitectura, configuración avanzada y documentación completa de la API, consulte el archivo [README.md](README.md).

Para guías de integración con servicios de automatización, revise la documentación en el directorio `docs/`.

