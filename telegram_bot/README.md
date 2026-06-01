# Bot de Telegram para API financiera

Bot de Telegram que proporciona reportes automatizados y gestión de transacciones del sistema de API financiera.

## Inicio rápido

### 1. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 2. Configuración del bot

**Paso 1: Crear el bot en Telegram**

- Abrir Telegram y buscar @BotFather
- Enviar el comando /newbot y seguir las instrucciones
- Guardar el token proporcionado

**Paso 2: Configurar variables de entorno**

```bash
cp .env.example .env
```

**Paso 3: Editar el archivo .env**

- Agregar el token de Telegram obtenido
- Agregar el ID de usuario de Telegram (obtenerlo desde @userinfobot)
- Configurar la URL de la API

### 3. Ejecución del bot

**Opción A - Mediante script:**
```bash
./start_bot.ps1  # Windows PowerShell
```

**Opción B - Ejecución directa:**
```bash
python bot.py
```

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| /start | Iniciar el bot y mostrar menú de comandos |
| /help | Ayuda detallada del sistema |
| /reporte_diario | Reporte de transacciones del día actual |
| /reporte_semanal | Reporte de últimos 7 días |
| /reporte_mensual | Reporte del mes en curso |
| /estadisticas | Estadísticas generales del sistema |
| /listar_transacciones | Últimas 10 transacciones registradas |
| /buscar_transaccion ID | Buscar transacción específica por ID |
| /cliente ID | Información detallada de un cliente |
| /portfolio | Reporte de portafolios de inversión |

## Autenticación y seguridad

Para restringir el acceso al bot a usuarios autorizados:

1. Obtener el ID de Telegram mediante @userinfobot
2. Agregar el ID al archivo .env:
   ```env
   AUTHORIZED_USERS=123456789,987654321
   ```

Nota: Si AUTHORIZED_USERS está vacío, el bot será público y cualquier usuario podrá utilizarlo.

## Configuración

Parámetros del archivo .env:

```env
# Token del bot (proporcionado por @BotFather)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrs...

# URL base de la API REST
API_BASE_URL=http://localhost:5000/api

# IDs de usuarios autorizados (separados por comas)
AUTHORIZED_USERS=123456789,987654321
```

## Resolución de problemas

### El bot no responde a los comandos

- Verificar que el token en .env sea correcto
- Confirmar que el proceso del bot esté en ejecución
- Revisar los logs en la consola para identificar errores

### Error de conexión a la API

- Verificar que la API esté ejecutándose: `python ../api/app.py`
- Confirmar que API_BASE_URL en .env sea la URL correcta
- Verificar conectividad de red al servidor de la API

### Mensaje "No estás autorizado para usar este bot"

- Verificar que el ID de usuario esté incluido en AUTHORIZED_USERS
- Confirmar el ID mediante @userinfobot en Telegram
- Reiniciar el bot después de modificar .env

## Estructura de archivos

```
telegram_bot/
├── bot.py                  # Bot principal
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de configuración
├── .env                   # Tu configuración (no subir a Git)
├── start_bot.ps1          # Script de inicio Windows
└── README.md              # Este archivo
```

## Dependencias

- `python-telegram-bot` - Framework para bots de Telegram
- `requests` - Cliente HTTP para consumir la API
- `python-dotenv` - Cargar variables de entorno

## Despliegue en producción

Para mantener el bot ejecutándose de forma continua, se pueden usar las siguientes opciones:

- **PythonAnywhere** (plan gratuito disponible)
- **Heroku** (planes gratuitos y de pago)
- **AWS/GCP/Azure** (planes de pago)
- **VPS propio** (planes de pago)

## Ejemplos de uso

```
# Ver estadísticas generales
/estadisticas

# Reporte del día
/reporte_diario

# Buscar una transacción
/buscar_transaccion 42

# Ver información de cliente
/cliente 5

# Listar últimas transacciones
/listar_transacciones
```

## Notas

- El bot solo funciona si la API está ejecutándose
- Los reportes se generan en tiempo real consultando la API
- Se puede ejecutar el bot en un ordenador local o en un servidor
