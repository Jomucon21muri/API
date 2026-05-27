# Bot de Telegram para API Financiera

Bot de Telegram que proporciona reportes y gestión de transacciones de la API financiera.

## 🚀 Inicio rápido

### 1. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 2. Configurar el bot

1. **Crear el bot en Telegram:**
   - Abre Telegram y busca `@BotFather`
   - Envía `/newbot` y sigue las instrucciones
   - Guarda el token que te proporcione

2. **Configurar variables de entorno:**
   ```powershell
   Copy-Item .env.example .env
   ```
   
3. **Editar el archivo `.env`:**
   - Abre `.env` y añade tu token de Telegram
   - Añade tu ID de Telegram (obtenerlo de @userinfobot)

### 3. Iniciar el bot

**Opción A - Usar el script:**
```powershell
.\start_bot.ps1
```

**Opción B - Manualmente:**
```powershell
python bot.py
```

## 📋 Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar el bot y ver comandos |
| `/help` | Ayuda detallada |
| `/reporte_diario` | Reporte de transacciones del día |
| `/reporte_semanal` | Reporte de últimos 7 días |
| `/reporte_mensual` | Reporte del mes actual |
| `/estadisticas` | Estadísticas generales del sistema |
| `/listar_transacciones` | Últimas 10 transacciones |
| `/buscar_transaccion ID` | Buscar transacción específica |
| `/cliente ID` | Información de un cliente |
| `/portfolio` | Reporte de portfolios |

## 🔐 Autenticación

Para permitir solo a ciertos usuarios usar el bot:

1. Obtén tu ID de Telegram con @userinfobot
2. Añádelo al archivo `.env`:
   ```env
   AUTHORIZED_USERS=123456789,987654321
   ```

Si dejas `AUTHORIZED_USERS` vacío, cualquiera podrá usar el bot.

## ⚙️ Configuración

Edita el archivo `.env`:

```env
# Token del bot (obtenido de @BotFather)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrs...

# URL de tu API
API_BASE_URL=http://localhost:5000/api

# IDs de usuarios autorizados (separados por comas)
AUTHORIZED_USERS=123456789,987654321
```

## 🔧 Solución de problemas

### El bot no responde
- Verifica que el token en `.env` sea correcto
- Asegúrate de que el bot esté ejecutándose
- Revisa los logs en la consola

### Error de conexión a la API
- Verifica que la API esté corriendo: `python ../api/app.py`
- Confirma que `API_BASE_URL` en `.env` sea correcta

### "No estás autorizado"
- Verifica que tu ID esté en `AUTHORIZED_USERS`
- Obtén tu ID con @userinfobot en Telegram

## 📚 Documentación completa

Ver [docs/bot-telegram-paso-a-paso.md](../docs/bot-telegram-paso-a-paso.md) para la guía completa paso a paso.

## 🛠️ Estructura de archivos

```
telegram_bot/
├── bot.py                  # Bot principal
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de configuración
├── .env                   # Tu configuración (no subir a Git)
├── start_bot.ps1          # Script de inicio Windows
└── README.md              # Este archivo
```

## 📦 Dependencias

- `python-telegram-bot` - Framework para bots de Telegram
- `requests` - Cliente HTTP para consumir la API
- `python-dotenv` - Cargar variables de entorno

## 🚀 Despliegue en producción

Para mantener el bot ejecutándose 24/7, puedes usar:

- **PythonAnywhere** (gratis)
- **Heroku** (gratis/pago)
- **AWS/GCP/Azure** (pago)
- **VPS propio** (pago)

Ver la guía completa en [docs/bot-telegram-paso-a-paso.md](../docs/bot-telegram-paso-a-paso.md#paso-7-desplegar-el-bot)

## 💡 Ejemplos de uso

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

## 📝 Notas

- El bot solo funciona si la API está ejecutándose
- Los reportes se generan en tiempo real consultando la API
- Puedes ejecutar el bot en tu PC o en un servidor
