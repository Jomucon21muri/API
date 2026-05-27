# Guía paso a paso: bot de Telegram para reportes y transacciones

Esta guía te llevará a crear un bot de Telegram que proporciona reportes y listas de transacciones de tu API financiera.

## Índice
1. [Requisitos previos](#requisitos-previos)
2. [Paso 1: Crear el bot en Telegram](#paso-1-crear-el-bot-en-telegram)
3. [Paso 2: Instalar dependencias](#paso-2-instalar-dependencias)
4. [Paso 3: Crear el bot básico](#paso-3-crear-el-bot-básico)
5. [Paso 4: Implementar comandos de reportes](#paso-4-implementar-comandos-de-reportes)
6. [Paso 5: Implementar listado de transacciones](#paso-5-implementar-listado-de-transacciones)
7. [Paso 6: Añadir autenticación](#paso-6-añadir-autenticación)
8. [Paso 7: Desplegar el bot](#paso-7-desplegar-el-bot)
9. [Comandos disponibles](#comandos-disponibles)

---

## Requisitos previos

- Python 3.9 o superior instalado
- API financiera funcionando (en local o desplegada)
- Cuenta de Telegram
- Editor de código (VS Code recomendado)

---

## Paso 1: Crear el bot en Telegram

### 1.1. Abrir BotFather
1. Abre Telegram en tu móvil o computadora
2. Busca `@BotFather` en el buscador
3. Inicia una conversación con `/start`

### 1.2. Crear el nuevo bot
```
/newbot
```

### 1.3. Configurar el bot
- **Nombre del bot**: Escribe un nombre para tu bot (ejemplo: "API Financiera Reporter")
- **Username del bot**: Debe terminar en 'bot' (ejemplo: "api_financiera_bot")

### 1.4. Guardar el token
BotFather te dará un token como este:
```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```
⚠️ **IMPORTANTE**: Guarda este token de forma segura, lo necesitarás más adelante.

### 1.5. Configurar comandos del bot
Para que los usuarios vean los comandos disponibles:
```
/setcommands
```
Selecciona tu bot y pega estos comandos:
```
start - Iniciar el bot
help - Mostrar ayuda
reporte_diario - Reporte de transacciones del día
reporte_semanal - Reporte de los últimos 7 días
reporte_mensual - Reporte del mes actual
listar_transacciones - Listar últimas 10 transacciones
buscar_transaccion - Buscar transacción por ID
cliente - Información de un cliente
estadisticas - Estadísticas generales
portfolio - Reporte de portfolios
```

---

## Paso 2: Instalar dependencias

### 2.1. Crear carpeta para el bot
```powershell
cd "c:\Users\muril\OneDrive - Universidad internacional de valencia\08MFPIAF_Automatización de Procesos Financieros\proyecto-api-financiera"
mkdir telegram_bot
cd telegram_bot
```

### 2.2. Crear archivo de dependencias
Crea el archivo `requirements.txt`:
```
python-telegram-bot==20.7
requests==2.31.0
python-dotenv==1.0.0
```

### 2.3. Instalar las dependencias
```powershell
pip install -r requirements.txt
```

---

## Paso 3: Crear el bot básico

### 3.1. Crear archivo de configuración
Crea el archivo `.env` en la carpeta `telegram_bot`:
```env
# Token del bot de Telegram
TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI

# URL de tu API (ajusta según tu configuración)
API_BASE_URL=http://localhost:5000/api

# Usuarios autorizados (IDs de Telegram separados por comas)
AUTHORIZED_USERS=123456789,987654321
```

⚠️ **Nota**: Reemplaza `TU_TOKEN_AQUI` con el token que te dio BotFather.

### 3.2. Crear el archivo principal del bot
Crea el archivo `telegram_bot/bot.py`:

```python
"""
Bot de Telegram para reportes de la API Financiera
"""

import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Cargar variables de entorno
load_dotenv()

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
AUTHORIZED_USERS = [int(uid) for uid in os.getenv('AUTHORIZED_USERS', '').split(',') if uid]

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ==================== FUNCIONES AUXILIARES ====================

def is_authorized(user_id: int) -> bool:
    """Verificar si el usuario está autorizado"""
    if not AUTHORIZED_USERS:
        return True  # Si no hay usuarios configurados, permitir a todos
    return user_id in AUTHORIZED_USERS


def format_money(amount: float, currency: str = 'USD') -> str:
    """Formatear cantidad de dinero"""
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def get_api(endpoint: str) -> dict:
    """Hacer petición GET a la API"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en petición a API: {e}")
        return {'error': str(e)}


# ==================== COMANDOS DEL BOT ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user = update.effective_user
    
    welcome_message = f"""
👋 ¡Hola {user.first_name}!

Soy el bot de reportes de la API Financiera.

📊 **Comandos disponibles:**

**Reportes:**
• /reporte_diario - Transacciones del día
• /reporte_semanal - Últimos 7 días
• /reporte_mensual - Mes actual
• /estadisticas - Estadísticas generales

**Transacciones:**
• /listar_transacciones - Últimas 10 transacciones
• /buscar_transaccion ID - Buscar por ID

**Clientes:**
• /cliente ID - Información de cliente

**Portfolio:**
• /portfolio - Reporte de portfolios

**Ayuda:**
• /help - Mostrar esta ayuda

---
Usa /help para más información.
    """
    
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
📖 **Guía de uso del bot**

**REPORTES**
• `/reporte_diario` - Muestra todas las transacciones del día actual con totales por estado
• `/reporte_semanal` - Transacciones de los últimos 7 días
• `/reporte_mensual` - Transacciones del mes en curso

**TRANSACCIONES**
• `/listar_transacciones` - Muestra las últimas 10 transacciones
• `/buscar_transaccion 123` - Busca la transacción con ID 123

**CLIENTES**
• `/cliente 5` - Muestra información del cliente con ID 5

**ESTADÍSTICAS**
• `/estadisticas` - Muestra un resumen general del sistema

**PORTFOLIO**
• `/portfolio` - Reporte consolidado de portfolios

---
💡 **Ejemplos:**
• `/buscar_transaccion 42`
• `/cliente 10`
    """
    
    await update.message.reply_text(help_text)


async def estadisticas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /estadisticas - Estadísticas generales"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado para usar este bot.")
        return
    
    await update.message.reply_text("📊 Generando estadísticas...")
    
    try:
        # Obtener datos de clientes
        customers_data = get_api('/customers?per_page=1000')
        if 'error' in customers_data:
            await update.message.reply_text(f"❌ Error al obtener clientes: {customers_data['error']}")
            return
        
        # Obtener transacciones recientes
        transactions_data = get_api('/transactions?per_page=1000')
        if 'error' in transactions_data:
            await update.message.reply_text(f"❌ Error al obtener transacciones: {transactions_data['error']}")
            return
        
        total_customers = customers_data.get('pagination', {}).get('total', 0)
        transactions = transactions_data.get('data', [])
        
        # Calcular estadísticas
        total_transactions = len(transactions)
        completed = sum(1 for t in transactions if t['estado'] == 'completed')
        pending = sum(1 for t in transactions if t['estado'] == 'pending')
        failed = sum(1 for t in transactions if t['estado'] == 'failed')
        
        total_amount = sum(float(t['monto']) for t in transactions if t['estado'] == 'completed')
        
        message = f"""
📊 **ESTADÍSTICAS GENERALES**

👥 **Clientes:**
• Total: {total_customers}

💰 **Transacciones:**
• Total: {total_transactions}
• Completadas: {completed}
• Pendientes: {pending}
• Fallidas: {failed}

💵 **Montos:**
• Total procesado: {format_money(total_amount)}
• Promedio: {format_money(total_amount/completed if completed > 0 else 0)}

📅 Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en estadisticas_command: {e}")
        await update.message.reply_text(f"❌ Error al generar estadísticas: {str(e)}")


# ==================== MAIN ====================

def main():
    """Iniciar el bot"""
    
    # Verificar configuración
    if not TELEGRAM_TOKEN:
        logger.error("ERROR: TELEGRAM_BOT_TOKEN no está configurado en .env")
        return
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Registrar comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("estadisticas", estadisticas_command))
    
    # Iniciar bot
    logger.info("🤖 Bot iniciado correctamente")
    print("=" * 50)
    print("🤖 BOT DE TELEGRAM INICIADO")
    print("=" * 50)
    print(f"📡 API: {API_BASE_URL}")
    print(f"👥 Usuarios autorizados: {len(AUTHORIZED_USERS) if AUTHORIZED_USERS else 'Todos'}")
    print("\n✅ El bot está ejecutándose. Presiona Ctrl+C para detener.")
    print("=" * 50)
    
    # Ejecutar bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
```

### 3.3. Probar el bot básico

1. **Asegúrate de que tu API esté corriendo:**
```powershell
cd ..\api
python app.py
```

2. **En otra terminal, inicia el bot:**
```powershell
cd ..\telegram_bot
python bot.py
```

3. **Abre Telegram y busca tu bot** (por el username que creaste)

4. **Envía el comando** `/start`

Si todo funciona, deberías ver un mensaje de bienvenida.

---

## Paso 4: Implementar comandos de reportes

Ahora vamos a añadir los comandos de reportes. Agrega estas funciones al archivo `bot.py`:

```python
# Añadir después de la función estadisticas_command

async def reporte_diario_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reporte_diario"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    await update.message.reply_text("📅 Generando reporte diario...")
    
    try:
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        data = get_api(f'/reports/daily?fecha={fecha_hoy}')
        
        if 'error' in data:
            await update.message.reply_text(f"❌ Error: {data['error']}")
            return
        
        report = data.get('data', {})
        
        message = f"""
📅 **REPORTE DIARIO - {report.get('fecha', fecha_hoy)}**

💰 **Totales:**
• Completadas: {format_money(report.get('total_completado', 0))}
• Pendientes: {format_money(report.get('total_pendiente', 0))}
• Fallidas: {format_money(report.get('total_fallido', 0))}

📊 **Cantidad de transacciones:**
• Completadas: {report.get('count_completado', 0)}
• Pendientes: {report.get('count_pendiente', 0)}
• Fallidas: {report.get('count_fallido', 0)}
• TOTAL: {report.get('total_transacciones', 0)}

💵 **Promedio:** {format_money(report.get('promedio_monto', 0))}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en reporte_diario: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def reporte_semanal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reporte_semanal"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    await update.message.reply_text("📊 Generando reporte semanal...")
    
    try:
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        data = get_api(f'/reports/transacciones?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
        
        if 'error' in data:
            await update.message.reply_text(f"❌ Error: {data['error']}")
            return
        
        report = data.get('data', {})
        
        message = f"""
📊 **REPORTE SEMANAL**
📅 {fecha_inicio} a {fecha_fin}

💰 **Totales por estado:**
• Completadas: {format_money(report.get('total_completado', 0))}
• Pendientes: {format_money(report.get('total_pendiente', 0))}
• Fallidas: {format_money(report.get('total_fallido', 0))}

📈 **Total general:** {format_money(report.get('total_general', 0))}

📊 **Transacciones:** {report.get('total_transacciones', 0)}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en reporte_semanal: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def reporte_mensual_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reporte_mensual"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    await update.message.reply_text("📊 Generando reporte mensual...")
    
    try:
        now = datetime.now()
        fecha_inicio = now.replace(day=1).strftime('%Y-%m-%d')
        fecha_fin = now.strftime('%Y-%m-%d')
        
        data = get_api(f'/reports/transacciones?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
        
        if 'error' in data:
            await update.message.reply_text(f"❌ Error: {data['error']}")
            return
        
        report = data.get('data', {})
        
        message = f"""
📊 **REPORTE MENSUAL - {now.strftime('%B %Y')}**
📅 {fecha_inicio} a {fecha_fin}

💰 **Totales por estado:**
• Completadas: {format_money(report.get('total_completado', 0))}
• Pendientes: {format_money(report.get('total_pendiente', 0))}
• Fallidas: {format_money(report.get('total_fallido', 0))}

📈 **Total general:** {format_money(report.get('total_general', 0))}

📊 **Transacciones:** {report.get('total_transacciones', 0)}

💵 **Promedio diario:** {format_money(report.get('total_general', 0) / now.day)}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en reporte_mensual: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /portfolio"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    await update.message.reply_text("💼 Generando reporte de portfolio...")
    
    try:
        data = get_api('/reports/portfolio')
        
        if 'error' in data:
            await update.message.reply_text(f"❌ Error: {data['error']}")
            return
        
        report = data.get('data', {})
        portfolios = report.get('portfolios', [])
        
        message = f"""
💼 **REPORTE DE PORTFOLIOS**

📊 **Totales:**
• Portfolios activos: {report.get('total_portfolios', 0)}
• Valor total: {format_money(report.get('valor_total', 0))}
• Total invertido: {format_money(report.get('total_invertido', 0))}
• Ganancia/Pérdida: {format_money(report.get('ganancia_perdida_total', 0))}

📈 **Top 5 portfolios:**
"""
        
        for i, portfolio in enumerate(portfolios[:5], 1):
            ganancia = portfolio.get('ganancia_perdida', 0)
            emoji = "📈" if ganancia >= 0 else "📉"
            message += f"\n{i}. {emoji} {portfolio.get('customer_nombre', 'N/A')}: {format_money(portfolio.get('valor_actual', 0))}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en portfolio: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")
```

**Registrar los nuevos comandos en la función `main()`:**

```python
# Busca la sección donde se registran los comandos y añade:
application.add_handler(CommandHandler("reporte_diario", reporte_diario_command))
application.add_handler(CommandHandler("reporte_semanal", reporte_semanal_command))
application.add_handler(CommandHandler("reporte_mensual", reporte_mensual_command))
application.add_handler(CommandHandler("portfolio", portfolio_command))
```

---

## Paso 5: Implementar listado de transacciones

Añade estas funciones para listar y buscar transacciones:

```python
# Añadir después de portfolio_command

async def listar_transacciones_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /listar_transacciones"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    await update.message.reply_text("📋 Obteniendo últimas transacciones...")
    
    try:
        data = get_api('/transactions?per_page=10&page=1')
        
        if 'error' in data:
            await update.message.reply_text(f"❌ Error: {data['error']}")
            return
        
        transactions = data.get('data', [])
        
        if not transactions:
            await update.message.reply_text("ℹ️ No hay transacciones registradas.")
            return
        
        message = "📋 **ÚLTIMAS 10 TRANSACCIONES**\n\n"
        
        for trans in transactions:
            estado_emoji = {
                'completed': '✅',
                'pending': '⏳',
                'failed': '❌',
                'cancelled': '🚫'
            }.get(trans['estado'], '❓')
            
            message += f"""
{estado_emoji} **ID {trans['id']}** - {trans.get('customer_nombre', 'N/A')}
💰 {format_money(trans['monto'], trans['moneda'])} | {trans['tipo']}
📅 {trans.get('fecha', 'N/A')[:10]}
---"""
        
        pagination = data.get('pagination', {})
        message += f"\n\n📄 Página 1 de {pagination.get('pages', 1)} | Total: {pagination.get('total', 0)}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en listar_transacciones: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def buscar_transaccion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar_transaccion ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    # Verificar que se proporcionó un ID
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "⚠️ Debes proporcionar un ID de transacción.\n\n"
            "Ejemplo: `/buscar_transaccion 42`"
        )
        return
    
    transaction_id = context.args[0]
    
    try:
        transaction_id = int(transaction_id)
    except ValueError:
        await update.message.reply_text("❌ El ID debe ser un número.")
        return
    
    await update.message.reply_text(f"🔍 Buscando transacción #{transaction_id}...")
    
    try:
        data = get_api(f'/transactions/{transaction_id}')
        
        if 'error' in data:
            await update.message.reply_text(f"❌ Transacción no encontrada: {data['error']}")
            return
        
        trans = data.get('data', {})
        
        estado_emoji = {
            'completed': '✅ Completada',
            'pending': '⏳ Pendiente',
            'failed': '❌ Fallida',
            'cancelled': '🚫 Cancelada'
        }.get(trans['estado'], '❓ Desconocido')
        
        message = f"""
🔍 **TRANSACCIÓN #{trans['id']}**

👤 **Cliente:** {trans.get('customer_nombre', 'N/A')} ({trans.get('customer_email', 'N/A')})

💰 **Monto:** {format_money(trans['monto'], trans['moneda'])}
📊 **Tipo:** {trans['tipo']}
📌 **Estado:** {estado_emoji}

📅 **Fecha:** {trans.get('fecha', 'N/A')}
✅ **Completada:** {trans.get('fecha_completado', 'No completada')}

📝 **Descripción:** {trans.get('descripcion', 'Sin descripción')}
🔗 **Referencia:** {trans.get('referencia_externa', 'N/A')}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en buscar_transaccion: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def cliente_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /cliente ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "⚠️ Debes proporcionar un ID de cliente.\n\n"
            "Ejemplo: `/cliente 5`"
        )
        return
    
    customer_id = context.args[0]
    
    try:
        customer_id = int(customer_id)
    except ValueError:
        await update.message.reply_text("❌ El ID debe ser un número.")
        return
    
    await update.message.reply_text(f"🔍 Buscando cliente #{customer_id}...")
    
    try:
        # Obtener información del cliente
        customer_data = get_api(f'/customers/{customer_id}')
        
        if 'error' in customer_data:
            await update.message.reply_text(f"❌ Cliente no encontrado: {customer_data['error']}")
            return
        
        customer = customer_data.get('data', {})
        
        # Obtener reporte del cliente
        report_data = get_api(f'/reports/customer/{customer_id}')
        report = report_data.get('data', {}) if 'data' in report_data else {}
        
        estado = "✅ Activo" if customer.get('activo') else "❌ Inactivo"
        
        message = f"""
👤 **CLIENTE #{customer['id']}**

📧 **Email:** {customer.get('email', 'N/A')}
👤 **Nombre:** {customer.get('nombre_completo', 'N/A')}
🌍 **País:** {customer.get('pais', 'N/A')}
📞 **Teléfono:** {customer.get('telefono', 'N/A')}
📌 **Estado:** {estado}

💰 **Estadísticas:**
• Transacciones: {report.get('total_transacciones', 0)}
• Total gastado: {format_money(report.get('total_monto', 0))}
• Promedio: {format_money(report.get('promedio_monto', 0))}
• En portfolio: {customer.get('total_acciones', 0)} posiciones

📅 **Registrado:** {customer.get('created_at', 'N/A')[:10]}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en cliente: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")
```

**Registrar estos comandos en `main()`:**

```python
application.add_handler(CommandHandler("listar_transacciones", listar_transacciones_command))
application.add_handler(CommandHandler("buscar_transaccion", buscar_transaccion_command))
application.add_handler(CommandHandler("cliente", cliente_command))
```

---

## Paso 6: Añadir autenticación

### 6.1. Obtener tu ID de Telegram

Para obtener tu ID de Telegram, usa el bot @userinfobot:
1. Busca `@userinfobot` en Telegram
2. Inicia conversación con `/start`
3. El bot te mostrará tu ID (ejemplo: `123456789`)

### 6.2. Configurar usuarios autorizados

Edita el archivo `.env` y añade los IDs autorizados:

```env
AUTHORIZED_USERS=123456789,987654321,555444333
```

Puedes añadir múltiples IDs separados por comas.

### 6.3. Probar la autenticación

El bot ya verifica la autorización en cada comando con:
```python
if not is_authorized(update.effective_user.id):
    await update.message.reply_text("❌ No estás autorizado.")
    return
```

---

## Paso 7: Desplegar el bot

### Opción A: Ejecutar en tu computadora

1. **Crear script de inicio** (`telegram_bot/start_bot.ps1`):
```powershell
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
    Write-Host "❌ ERROR: No se encuentra el archivo .env" -ForegroundColor Red
    Write-Host "Crea el archivo .env con tu token de Telegram" -ForegroundColor Yellow
    pause
    exit
}

# Iniciar el bot
Write-Host "`n🤖 Iniciando bot..." -ForegroundColor Green
python bot.py
```

2. **Ejecutar el script:**
```powershell
cd telegram_bot
.\start_bot.ps1
```

### Opción B: Ejecutar como servicio en segundo plano

1. **Crear script para ejecutar en segundo plano** (`telegram_bot/start_bot_background.ps1`):

```powershell
# Iniciar bot en segundo plano

$botPath = "$PSScriptRoot\bot.py"

# Iniciar proceso en segundo plano
Start-Process -FilePath "python" -ArgumentList $botPath -WindowStyle Hidden

Write-Host "✅ Bot iniciado en segundo plano" -ForegroundColor Green
Write-Host "Para detenerlo, busca el proceso 'python' en el Administrador de tareas" -ForegroundColor Yellow
```

### Opción C: Desplegar en servidor (PythonAnywhere, Heroku, AWS, etc.)

Ver sección adicional al final de este documento.

---

## Comandos disponibles

Una vez que el bot esté funcionando, estos son los comandos que puedes usar:

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Iniciar el bot | `/start` |
| `/help` | Mostrar ayuda | `/help` |
| `/reporte_diario` | Reporte del día actual | `/reporte_diario` |
| `/reporte_semanal` | Reporte de últimos 7 días | `/reporte_semanal` |
| `/reporte_mensual` | Reporte del mes | `/reporte_mensual` |
| `/estadisticas` | Estadísticas generales | `/estadisticas` |
| `/listar_transacciones` | Últimas 10 transacciones | `/listar_transacciones` |
| `/buscar_transaccion ID` | Buscar transacción por ID | `/buscar_transaccion 42` |
| `/cliente ID` | Información de cliente | `/cliente 5` |
| `/portfolio` | Reporte de portfolios | `/portfolio` |

---

## Solución de problemas

### El bot no responde
- Verifica que el token en `.env` sea correcto
- Asegúrate de que el script esté ejecutándose sin errores
- Revisa los logs en la consola

### Error de conexión a la API
- Verifica que la API esté corriendo (`python api/app.py`)
- Confirma que la URL en `.env` sea correcta
- Si la API está en otro servidor, asegúrate de que sea accesible

### "No estás autorizado"
- Verifica que tu ID de Telegram esté en `AUTHORIZED_USERS` en `.env`
- Obtén tu ID con @userinfobot

### Errores al instalar dependencias
```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar de nuevo
pip install -r requirements.txt
```

---

## Próximos pasos y mejoras

### Funcionalidades adicionales que puedes añadir:

1. **Notificaciones automáticas:**
   - Alertas cuando haya transacciones grandes
   - Notificaciones de transacciones fallidas
   - Reportes programados diarios/semanales

2. **Botones interactivos:**
   - Usar InlineKeyboard para navegación
   - Botones para filtrar reportes
   - Confirmaciones para acciones

3. **Exportar reportes:**
   - Generar PDF o Excel
   - Enviar archivos por Telegram

4. **Comandos de administración:**
   - Crear transacciones desde Telegram
   - Actualizar estados
   - Gestionar clientes

5. **Gráficos y visualizaciones:**
   - Generar gráficos con matplotlib
   - Enviar imágenes de estadísticas

---

## Recursos adicionales

- **Documentación python-telegram-bot:** https://docs.python-telegram-bot.org/
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **BotFather:** https://t.me/BotFather

---

## Apéndice: Desplegar en PythonAnywhere (gratis)

### 1. Crear cuenta en PythonAnywhere
- Ir a https://www.pythonanywhere.com
- Crear cuenta gratuita

### 2. Subir archivos
- Subir `bot.py` y `.env`
- Subir `requirements.txt`

### 3. Instalar dependencias
En la consola de PythonAnywhere:
```bash
pip3 install --user -r requirements.txt
```

### 4. Crear tarea programada
- Ir a "Tasks"
- Crear nueva tarea con el comando: `python3 /home/tuusuario/bot.py`

¡Y listo! Tu bot estará funcionando 24/7 de forma gratuita.

---

**¡Felicidades! 🎉 Ahora tienes un bot de Telegram completamente funcional para gestionar tu API financiera.**
