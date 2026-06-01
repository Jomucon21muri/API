"""
Bot de Telegram para gestión del sistema financiero.

Este módulo implementa un bot de Telegram que proporciona acceso a los
datos y reportes del sistema de gestión financiera a través de comandos
interactivos con menús y botones.

Funcionalidades principales:
    - Reportes diarios, semanales y mensuales
    - Consulta de transacciones y clientes
    - Visualización de portafolios
    - Estadísticas del sistema
    - Autenticación de usuarios autorizados

Comandos disponibles:
    /start - Iniciar el bot y mostrar menú principal
    /menu - Mostrar menú de navegación
    /help - Ayuda y lista de comandos
    /ping - Verificar estado del sistema
    /estadisticas - Estadísticas globales
    /reporte_diario - Reporte de transacciones del día
    /reporte_semanal - Reporte semanal
    /reporte_mensual - Reporte mensual
    /transacciones - Listar transacciones recientes
    /clientes - Listar clientes
    /portfolio - Ver portafolios

Variables de entorno requeridas:
    TELEGRAM_BOT_TOKEN: Token del bot de Telegram
    API_BASE_URL: URL base de la API (default: http://localhost:5000/api)
    API_KEY: Clave de autenticación de la API
    AUTHORIZED_USERS: IDs de usuarios autorizados (separados por comas)
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# Cargar variables de entorno
load_dotenv()

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
API_KEY = os.getenv('API_KEY', 'api_key_demo_12345')
AUTHORIZED_USERS_STR = os.getenv('AUTHORIZED_USERS', '')
AUTHORIZED_USERS = [int(uid.strip()) for uid in AUTHORIZED_USERS_STR.split(',') if uid.strip()]

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ==================== FUNCIONES AUXILIARES ====================

def is_authorized(user_id: int) -> bool:
    """
    Verifica si un usuario está autorizado para usar el bot.
    
    Args:
        user_id: ID del usuario de Telegram
        
    Returns:
        True si el usuario está autorizado, False en caso contrario.
        Si AUTHORIZED_USERS está vacío, todos los usuarios están autorizados.
    """
    if not AUTHORIZED_USERS:
        return True
    return user_id in AUTHORIZED_USERS


def get_api(endpoint: str) -> Dict[str, Any]:
    """
    Realiza una petición GET a la API del sistema.
    
    Args:
        endpoint: Ruta del endpoint (ejemplo: '/transactions')
        
    Returns:
        Dict con la respuesta JSON de la API o dict con clave 'error'
    """
    try:
        url = f"{API_BASE_URL}{endpoint}"
        headers = {'X-API-Key': API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'Error en petición API {endpoint}: {e}')
        return {'error': str(e)}
    except Exception as e:
        logger.error(f'Error inesperado en petición API: {e}')
        return {'error': str(e)}


def format_money(amount: float, currency: str = 'USD') -> str:
    """
    Formatea una cantidad monetaria con su símbolo correspondiente.
    
    Args:
        amount: Cantidad a formatear
        currency: Código de moneda (USD, EUR, GBP, etc.)
        
    Returns:
        String formateado con símbolo de moneda y separadores de miles
    """
    symbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 
        'MXN': '$', 'JPY': '¥', 'BRL': 'R$'
    }
    symbol = symbols.get(currency, '$')
    return f"{symbol}{amount:,.2f}"


# ==================== COMANDOS PRINCIPALES ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Comando /start - Inicia el bot y muestra el menú principal.
    
    Presenta un menú interactivo con botones para acceder a las diferentes
    funcionalidades del bot.
    
    Args:
        update: Objeto Update de Telegram
        context: Contexto de la conversación
    """
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("Reportes", callback_data='menu_reportes'),
            InlineKeyboardButton("Transacciones", callback_data='menu_transacciones')
        ],
        [
            InlineKeyboardButton("Clientes", callback_data='menu_clientes'),
            InlineKeyboardButton("Portfolio", callback_data='menu_portfolio')
        ],
        [
            InlineKeyboardButton("Stocks", callback_data='menu_stocks'),
            InlineKeyboardButton("Estadísticas", callback_data='estadisticas')
        ],
        [
            InlineKeyboardButton("Ayuda", callback_data='help'),
            InlineKeyboardButton("Ver Dashboard", url='https://jomucon21muri.github.io/API/')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
Hola {user.first_name}

Bienvenido al bot del sistema de gestión financiera.

Utilice los botones del menú o escriba /help para ver todos los comandos disponibles.

Dashboard web: https://jomucon21muri.github.io/API/
    """
    
    logger.info(f'Usuario {user.id} ({user.first_name}) inició el bot')
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /menu - Mostrar menu principal"""
    keyboard = [
        [
            InlineKeyboardButton("Reportes", callback_data='menu_reportes'),
            InlineKeyboardButton("Transacciones", callback_data='menu_transacciones')
        ],
        [
            InlineKeyboardButton("Clientes", callback_data='menu_clientes'),
            InlineKeyboardButton("Portfolio", callback_data='menu_portfolio')
        ],
        [
            InlineKeyboardButton("Stocks", callback_data='menu_stocks'),
            InlineKeyboardButton("Estadisticas", callback_data='estadisticas')
        ],
        [
            InlineKeyboardButton("Ayuda", callback_data='help'),
            InlineKeyboardButton("Ver Dashboard", url='https://jomucon21muri.github.io/API/')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("MENU PRINCIPAL\n\nSelecciona una opcion:", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
**COMANDOS DISPONIBLES**

**Menu:**
/start - Iniciar bot y mostrar menu
/menu - Mostrar menu interactivo
/help - Esta ayuda
/ping - Verificar conexion

**Reportes:**
/reporte_diario - Transacciones de hoy
/reporte_semanal - Ultimos 7 dias
/reporte_mensual - Mes actual
/estadisticas - Estadisticas generales

**Transacciones:**
/listar_transacciones - Ultimas 10
/transacciones_pendientes - Solo pendientes
/transacciones_completadas - Solo completadas
/buscar_transaccion ID - Buscar por ID

**Clientes:**
/listar_clientes - Lista de clientes
/top_clientes - Top 10 clientes
/cliente ID - Info de un cliente

**Portfolio:**
/portfolio - Reporte general
/portfolio_cliente ID - Portfolio de cliente
/top_portfolios - Mejores portfolios

**Stocks:**
/stocks - Lista de acciones
/stock SIMBOLO - Info de accion (ej: /stock AAPL)

**Ejemplos:**
/buscar_transaccion 42
/cliente 5
/stock TSLA
/portfolio_cliente 10
    """
    await update.message.reply_text(help_text)


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ping - Verificar conexion"""
    try:
        data = get_api('/health')
        
        if 'error' in data:
            await update.message.reply_text(f"[ERROR] API no responde\n\n{data['error']}")
            return
        
        status = data.get('status', 'unknown')
        db_status = data.get('database', 'unknown')
        version = data.get('version', 'N/A')
        
        message = f"""
[OK] Conexion exitosa

Estado: {status}
Base de datos: {db_status}
Version: {version}
URL: {API_BASE_URL}

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"[ERROR] {str(e)}")


# ==================== ESTADISTICAS ====================

async def estadisticas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /estadisticas"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Generando estadisticas...")
    
    try:
        customers_data = get_api('/customers?per_page=1000')
        transactions_data = get_api('/transactions?per_page=1000')
        
        if 'error' in customers_data or 'error' in transactions_data:
            await update.message.reply_text("Error al obtener datos.")
            return
        
        total_customers = customers_data.get('pagination', {}).get('total', 0)
        transactions = transactions_data.get('data', [])
        
        total_transactions = len(transactions)
        completed = sum(1 for t in transactions if t['estado'] == 'completed')
        pending = sum(1 for t in transactions if t['estado'] == 'pending')
        failed = sum(1 for t in transactions if t['estado'] == 'failed')
        
        total_amount = sum(float(t['monto']) for t in transactions if t['estado'] == 'completed')
        
        message = f"""
**ESTADISTICAS GENERALES**

**Clientes:** {total_customers}

**Transacciones:**
Total: {total_transactions}
Completadas: {completed}
Pendientes: {pending}
Fallidas: {failed}

**Montos:**
Total procesado: {format_money(total_amount)}
Promedio: {format_money(total_amount/completed if completed > 0 else 0)}

Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en estadisticas: {e}")
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== REPORTES ====================

async def reporte_diario_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reporte_diario"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Generando reporte diario...")
    
    try:
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        data = get_api(f'/reports/daily?fecha={fecha_hoy}')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        report = data.get('data', {})
        
        message = f"""
**REPORTE DIARIO**
{report.get('fecha', fecha_hoy)}

**Totales:**
Completadas: {format_money(report.get('total_completado', 0))}
Pendientes: {format_money(report.get('total_pendiente', 0))}
Fallidas: {format_money(report.get('total_fallido', 0))}

**Cantidad:**
Completadas: {report.get('count_completado', 0)}
Pendientes: {report.get('count_pendiente', 0)}
Fallidas: {report.get('count_fallido', 0)}
TOTAL: {report.get('total_transacciones', 0)}

**Promedio:** {format_money(report.get('promedio_monto', 0))}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def reporte_semanal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reporte_semanal"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Generando reporte semanal...")
    
    try:
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        data = get_api(f'/reports/transacciones?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        report = data.get('data', {})
        
        message = f"""
**REPORTE SEMANAL**
{fecha_inicio} a {fecha_fin}

**Totales por estado:**
Completadas: {format_money(report.get('total_completado', 0))}
Pendientes: {format_money(report.get('total_pendiente', 0))}
Fallidas: {format_money(report.get('total_fallido', 0))}

**Total general:** {format_money(report.get('total_general', 0))}

**Transacciones:** {report.get('total_transacciones', 0)}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def reporte_mensual_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /reporte_mensual"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Generando reporte mensual...")
    
    try:
        now = datetime.now()
        fecha_inicio = now.replace(day=1).strftime('%Y-%m-%d')
        fecha_fin = now.strftime('%Y-%m-%d')
        
        data = get_api(f'/reports/transacciones?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        report = data.get('data', {})
        
        message = f"""
**REPORTE MENSUAL**
{now.strftime('%B %Y')}

**Totales por estado:**
Completadas: {format_money(report.get('total_completado', 0))}
Pendientes: {format_money(report.get('total_pendiente', 0))}
Fallidas: {format_money(report.get('total_fallido', 0))}

**Total general:** {format_money(report.get('total_general', 0))}

**Transacciones:** {report.get('total_transacciones', 0)}

**Promedio diario:** {format_money(report.get('total_general', 0) / now.day if now.day > 0 else 0)}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== TRANSACCIONES ====================

async def listar_transacciones_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /listar_transacciones"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Obteniendo transacciones...")
    
    try:
        data = get_api('/transactions?per_page=10&page=1')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        transactions = data.get('data', [])
        
        if not transactions:
            await update.message.reply_text("No hay transacciones.")
            return
        
        message = "**ULTIMAS 10 TRANSACCIONES**\n\n"
        
        for trans in transactions:
            estado_texto = {
                'completed': '[OK]',
                'pending': '[PEND]',
                'failed': '[FAIL]',
                'cancelled': '[CANC]'
            }.get(trans['estado'], '[?]')
            
            message += f"""
{estado_texto} **ID {trans['id']}** - {trans.get('customer_nombre', 'N/A')}
{format_money(trans['monto'], trans['moneda'])} | {trans['tipo']}
Fecha: {trans.get('fecha', 'N/A')[:10]}
---"""
        
        pagination = data.get('pagination', {})
        message += f"\n\nPagina 1 de {pagination.get('pages', 1)} | Total: {pagination.get('total', 0)}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def transacciones_pendientes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /transacciones_pendientes"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    try:
        data = get_api('/transactions?estado=pending&per_page=10')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        transactions = data.get('data', [])
        
        if not transactions:
            await update.message.reply_text("No hay transacciones pendientes.")
            return
        
        message = "**TRANSACCIONES PENDIENTES**\n\n"
        
        for trans in transactions:
            message += f"""
[PEND] **ID {trans['id']}** - {trans.get('customer_nombre', 'N/A')}
{format_money(trans['monto'], trans['moneda'])} | {trans['tipo']}
Fecha: {trans.get('fecha', 'N/A')[:10]}
---"""
        
        pagination = data.get('pagination', {})
        message += f"\n\nTotal pendientes: {pagination.get('total', 0)}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def transacciones_completadas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /transacciones_completadas"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    try:
        data = get_api('/transactions?estado=completed&per_page=10')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        transactions = data.get('data', [])
        
        if not transactions:
            await update.message.reply_text("No hay transacciones completadas recientes.")
            return
        
        message = "**ULTIMAS TRANSACCIONES COMPLETADAS**\n\n"
        
        for trans in transactions:
            message += f"""
[OK] **ID {trans['id']}** - {trans.get('customer_nombre', 'N/A')}
{format_money(trans['monto'], trans['moneda'])} | {trans['tipo']}
Fecha: {trans.get('fecha', 'N/A')[:10]}
---"""
        
        pagination = data.get('pagination', {})
        message += f"\n\nTotal completadas: {pagination.get('total', 0)}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def buscar_transaccion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar_transaccion ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Debes proporcionar un ID.\n\nEjemplo: /buscar_transaccion 42")
        return
    
    transaction_id = context.args[0]
    
    try:
        transaction_id = int(transaction_id)
    except ValueError:
        await update.message.reply_text("El ID debe ser un numero.")
        return
    
    await update.message.reply_text(f"Buscando transaccion #{transaction_id}...")
    
    try:
        data = get_api(f'/transactions/{transaction_id}')
        
        if 'error' in data:
            await update.message.reply_text(f"Transaccion no encontrada: {data['error']}")
            return
        
        trans = data.get('data', {})
        
        estado_texto = {
            'completed': '[OK]',
            'pending': '[PEND]',
            'failed': '[FAIL]',
            'cancelled': '[CANC]'
        }.get(trans['estado'], '[?]')
        
        message = f"""
**TRANSACCION #{trans['id']}**

{estado_texto} **{trans['tipo'].upper()}**

**Cliente:** {trans.get('customer_nombre', 'N/A')} (ID: {trans.get('customer_id')})
**Monto:** {format_money(trans['monto'], trans['moneda'])}
**Estado:** {trans['estado']}
**Descripcion:** {trans.get('descripcion', 'N/A')}
**Fecha:** {trans.get('fecha', 'N/A')}
**Creado:** {trans.get('created_at', 'N/A')[:19]}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== CLIENTES ====================

async def listar_clientes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /listar_clientes"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    try:
        data = get_api('/customers?per_page=10&page=1')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        customers = data.get('data', [])
        
        if not customers:
            await update.message.reply_text("No hay clientes.")
            return
        
        message = "**LISTA DE CLIENTES**\n\n"
        
        for customer in customers:
            estado = "Activo" if customer.get('activo') else "Inactivo"
            message += f"""
**ID {customer['id']}** - {customer.get('nombre_completo', 'N/A')}
Email: {customer.get('email', 'N/A')}
Pais: {customer.get('pais', 'N/A')} | {estado}
---"""
        
        pagination = data.get('pagination', {})
        message += f"\n\nPagina 1 de {pagination.get('pages', 1)} | Total: {pagination.get('total', 0)}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def top_clientes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /top_clientes"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    try:
        data = get_api('/reports/top-customers?limit=10')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        customers = data.get('data', [])
        
        if not customers:
            await update.message.reply_text("No hay datos.")
            return
        
        message = "**TOP 10 CLIENTES**\n\n"
        
        for i, customer in enumerate(customers, 1):
            message += f"""
{i}. **{customer.get('nombre', 'N/A')}**
   Transacciones: {customer.get('total_transacciones', 0)}
   Total: {format_money(customer.get('total_monto', 0))}
---"""
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def cliente_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /cliente ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Debes proporcionar un ID.\n\nEjemplo: /cliente 5")
        return
    
    customer_id = context.args[0]
    
    try:
        customer_id = int(customer_id)
    except ValueError:
        await update.message.reply_text("El ID debe ser un numero.")
        return
    
    await update.message.reply_text(f"Obteniendo cliente #{customer_id}...")
    
    try:
        data = get_api(f'/customers/{customer_id}')
        
        if 'error' in data:
            await update.message.reply_text(f"Cliente no encontrado: {data['error']}")
            return
        
        customer = data.get('data', {})
        estado = "Activo" if customer.get('activo') else "Inactivo"
        
        message = f"""
**CLIENTE #{customer['id']}**

**Nombre:** {customer.get('nombre_completo', 'N/A')}
**Email:** {customer.get('email', 'N/A')}
**Telefono:** {customer.get('telefono', 'N/A')}

**Ubicacion:**
Pais: {customer.get('pais', 'N/A')}
Ciudad: {customer.get('ciudad', 'N/A')}

**Estado:** {estado}
**Registrado:** {customer.get('created_at', 'N/A')[:10]}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== PORTFOLIO ====================

async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /portfolio"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Generando reporte de portfolio...")
    
    try:
        data = get_api('/reports/portfolio')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        report = data.get('data', {})
        portfolios = report.get('portfolios', [])
        
        message = f"""
**REPORTE DE PORTFOLIOS**

**Totales:**
Portfolios activos: {report.get('total_portfolios', 0)}
Valor total: {format_money(report.get('valor_total', 0))}
Total invertido: {format_money(report.get('total_invertido', 0))}
Ganancia/Perdida: {format_money(report.get('ganancia_perdida_total', 0))}

**Top 5 portfolios:**
"""
        
        for i, portfolio in enumerate(portfolios[:5], 1):
            ganancia = portfolio.get('ganancia_perdida', 0)
            indicador = "[+]" if ganancia >= 0 else "[-]"
            message += f"\n{i}. {indicador} {portfolio.get('customer_nombre', 'N/A')}: {format_money(portfolio.get('valor_actual', 0))}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def top_portfolios_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /top_portfolios"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    try:
        data = get_api('/reports/portfolio')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        portfolios = data.get('data', {}).get('portfolios', [])
        
        if not portfolios:
            await update.message.reply_text("No hay portfolios.")
            return
        
        portfolios_sorted = sorted(portfolios, key=lambda x: x.get('ganancia_perdida', 0), reverse=True)
        
        message = "**TOP 10 PORTFOLIOS**\n\n"
        
        for i, portfolio in enumerate(portfolios_sorted[:10], 1):
            ganancia = portfolio.get('ganancia_perdida', 0)
            rendimiento = portfolio.get('rendimiento_porcentaje', 0)
            indicador = "[+]" if ganancia >= 0 else "[-]"
            message += f"""
{i}. {indicador} **{portfolio.get('customer_nombre', 'N/A')}**
   Valor: {format_money(portfolio.get('valor_actual', 0))}
   Ganancia: {format_money(ganancia)}
   Rendimiento: {rendimiento:.2f}%
---"""
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def portfolio_cliente_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /portfolio_cliente ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Debes proporcionar un ID.\n\nEjemplo: /portfolio_cliente 5")
        return
    
    customer_id = context.args[0]
    
    try:
        customer_id = int(customer_id)
    except ValueError:
        await update.message.reply_text("El ID debe ser un numero.")
        return
    
    await update.message.reply_text(f"Obteniendo portfolio del cliente #{customer_id}...")
    
    try:
        data = get_api(f'/portfolio/customer/{customer_id}')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        portfolio = data.get('data', {})
        posiciones = portfolio.get('posiciones', [])
        
        valor_total = portfolio.get('valor_total', 0)
        ganancia = portfolio.get('ganancia_perdida_total', 0)
        rendimiento = portfolio.get('rendimiento_porcentaje', 0)
        
        message = f"""
**PORTFOLIO CLIENTE #{customer_id}**

**Resumen:**
Valor total: {format_money(valor_total)}
Total invertido: {format_money(portfolio.get('total_invertido', 0))}
Ganancia/Perdida: {format_money(ganancia)}
Rendimiento: {rendimiento:.2f}%

**Posiciones ({len(posiciones)}):**
"""
        
        for pos in posiciones[:10]:
            ganancia_pos = pos.get('ganancia_perdida', 0)
            indicador = "[+]" if ganancia_pos >= 0 else "[-]"
            message += f"""
{indicador} {pos.get('simbolo', 'N/A')} x {pos.get('cantidad', 0)}
   Precio actual: {format_money(pos.get('precio_actual', 0))}
   Ganancia: {format_money(ganancia_pos)}
"""
        
        if len(posiciones) > 10:
            message += f"\n... y {len(posiciones) - 10} posiciones mas"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== STOCKS ====================

async def stocks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stocks"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Obteniendo acciones...")
    
    try:
        data = get_api('/stocks?per_page=15')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        stocks = data.get('data', [])
        
        if not stocks:
            await update.message.reply_text("No hay acciones disponibles.")
            return
        
        message = "**ACCIONES DISPONIBLES**\n\n"
        
        for stock in stocks:
            cambio = stock.get('cambio_porcentaje', 0)
            indicador = "[+]" if cambio >= 0 else "[-]"
            message += f"""
{indicador} **{stock.get('simbolo', 'N/A')}** - {stock.get('nombre', 'N/A')}
   Precio: {format_money(stock.get('precio_actual', 0))}
   Cambio: {cambio:.2f}%
---"""
        
        message += "\n\nUsa /stock SIMBOLO para ver detalles"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stock SIMBOLO"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Debes proporcionar un simbolo.\n\nEjemplo: /stock AAPL")
        return
    
    simbolo = context.args[0].upper()
    
    await update.message.reply_text(f"Obteniendo informacion de {simbolo}...")
    
    try:
        data = get_api(f'/stocks/{simbolo}')
        
        if 'error' in data:
            await update.message.reply_text(f"Accion no encontrada: {data['error']}")
            return
        
        stock = data.get('data', {})
        
        cambio = stock.get('cambio_porcentaje', 0)
        indicador = "[+]" if cambio >= 0 else "[-]"
        
        message = f"""
**{stock.get('simbolo', 'N/A')}** - {stock.get('nombre', 'N/A')}

**Precio actual:** {format_money(stock.get('precio_actual', 0))}
**Cambio:** {indicador} {cambio:.2f}%

**Mercado:**
Apertura: {format_money(stock.get('precio_apertura', 0))}
Maximo: {format_money(stock.get('precio_maximo', 0))}
Minimo: {format_money(stock.get('precio_minimo', 0))}
Cierre anterior: {format_money(stock.get('precio_cierre_anterior', 0))}

**Volumen:** {stock.get('volumen', 0):,}
**Sector:** {stock.get('sector', 'N/A')}

**Actualizado:** {stock.get('ultima_actualizacion', 'N/A')[:16]}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== CALLBACK HANDLERS ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar clicks en botones"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'menu_reportes':
        keyboard = [
            [InlineKeyboardButton("Reporte Diario", callback_data='cmd_reporte_diario')],
            [InlineKeyboardButton("Reporte Semanal", callback_data='cmd_reporte_semanal')],
            [InlineKeyboardButton("Reporte Mensual", callback_data='cmd_reporte_mensual')],
            [InlineKeyboardButton("Volver", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU DE REPORTES**\n\nSelecciona el tipo de reporte:", reply_markup=reply_markup)
    
    elif query.data == 'menu_transacciones':
        keyboard = [
            [InlineKeyboardButton("Ultimas Transacciones", callback_data='cmd_listar_transacciones')],
            [InlineKeyboardButton("Pendientes", callback_data='cmd_transacciones_pendientes')],
            [InlineKeyboardButton("Completadas", callback_data='cmd_transacciones_completadas')],
            [InlineKeyboardButton("Volver", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU DE TRANSACCIONES**\n\nSelecciona una opcion:", reply_markup=reply_markup)
    
    elif query.data == 'menu_clientes':
        keyboard = [
            [InlineKeyboardButton("Listar Clientes", callback_data='cmd_listar_clientes')],
            [InlineKeyboardButton("Top Clientes", callback_data='cmd_top_clientes')],
            [InlineKeyboardButton("Volver", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU DE CLIENTES**\n\nSelecciona una opcion:", reply_markup=reply_markup)
    
    elif query.data == 'menu_portfolio':
        keyboard = [
            [InlineKeyboardButton("Reporte Portfolio", callback_data='cmd_portfolio')],
            [InlineKeyboardButton("Top Portfolios", callback_data='cmd_top_portfolios')],
            [InlineKeyboardButton("Volver", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU DE PORTFOLIO**\n\nSelecciona una opcion:", reply_markup=reply_markup)
    
    elif query.data == 'menu_stocks':
        keyboard = [
            [InlineKeyboardButton("Lista de Stocks", callback_data='cmd_stocks')],
            [InlineKeyboardButton("Volver", callback_data='menu_principal')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU DE STOCKS**\n\nSelecciona una opcion:", reply_markup=reply_markup)
    
    elif query.data == 'estadisticas':
        await query.edit_message_text("Generando estadisticas...")
        temp_update = Update(update_id=update.update_id, message=query.message)
        temp_update.message.reply_text = query.message.reply_text
        await estadisticas_command(temp_update, context)
    
    elif query.data == 'help':
        await help_command(Update(update_id=update.update_id, message=query.message), context)
    
    elif query.data == 'menu_principal':
        keyboard = [
            [
                InlineKeyboardButton("Reportes", callback_data='menu_reportes'),
                InlineKeyboardButton("Transacciones", callback_data='menu_transacciones')
            ],
            [
                InlineKeyboardButton("Clientes", callback_data='menu_clientes'),
                InlineKeyboardButton("Portfolio", callback_data='menu_portfolio')
            ],
            [
                InlineKeyboardButton("Stocks", callback_data='menu_stocks'),
                InlineKeyboardButton("Estadisticas", callback_data='estadisticas')
            ],
            [
                InlineKeyboardButton("Ayuda", callback_data='help'),
                InlineKeyboardButton("Ver Dashboard", url='https://jomucon21muri.github.io/API/')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU PRINCIPAL**\n\nSelecciona una opcion:", reply_markup=reply_markup)
    
    elif query.data.startswith('cmd_'):
        command = query.data.replace('cmd_', '')
        await query.edit_message_text(f"Ejecutando {command}...")
        
        temp_update = Update(update_id=update.update_id, message=query.message)
        temp_update.message.reply_text = query.message.reply_text
        
        if command == 'reporte_diario':
            await reporte_diario_command(temp_update, context)
        elif command == 'reporte_semanal':
            await reporte_semanal_command(temp_update, context)
        elif command == 'reporte_mensual':
            await reporte_mensual_command(temp_update, context)
        elif command == 'listar_transacciones':
            await listar_transacciones_command(temp_update, context)
        elif command == 'transacciones_pendientes':
            await transacciones_pendientes_command(temp_update, context)
        elif command == 'transacciones_completadas':
            await transacciones_completadas_command(temp_update, context)
        elif command == 'listar_clientes':
            await listar_clientes_command(temp_update, context)
        elif command == 'top_clientes':
            await top_clientes_command(temp_update, context)
        elif command == 'portfolio':
            await portfolio_command(temp_update, context)
        elif command == 'top_portfolios':
            await top_portfolios_command(temp_update, context)
        elif command == 'stocks':
            await stocks_command(temp_update, context)


# ==================== MAIN ====================

def main():
    """Iniciar el bot"""
    
    if not TELEGRAM_TOKEN:
        logger.error("ERROR: TELEGRAM_BOT_TOKEN no configurado")
        print("\nERROR: TELEGRAM_BOT_TOKEN no esta configurado en .env")
        return
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Registrar comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    
    # Reportes
    application.add_handler(CommandHandler("estadisticas", estadisticas_command))
    application.add_handler(CommandHandler("reporte_diario", reporte_diario_command))
    application.add_handler(CommandHandler("reporte_semanal", reporte_semanal_command))
    application.add_handler(CommandHandler("reporte_mensual", reporte_mensual_command))
    
    # Transacciones
    application.add_handler(CommandHandler("listar_transacciones", listar_transacciones_command))
    application.add_handler(CommandHandler("transacciones_pendientes", transacciones_pendientes_command))
    application.add_handler(CommandHandler("transacciones_completadas", transacciones_completadas_command))
    application.add_handler(CommandHandler("buscar_transaccion", buscar_transaccion_command))
    
    # Clientes
    application.add_handler(CommandHandler("listar_clientes", listar_clientes_command))
    application.add_handler(CommandHandler("top_clientes", top_clientes_command))
    application.add_handler(CommandHandler("cliente", cliente_command))
    
    # Portfolio
    application.add_handler(CommandHandler("portfolio", portfolio_command))
    application.add_handler(CommandHandler("portfolio_cliente", portfolio_cliente_command))
    application.add_handler(CommandHandler("top_portfolios", top_portfolios_command))
    
    # Stocks
    application.add_handler(CommandHandler("stocks", stocks_command))
    application.add_handler(CommandHandler("stock", stock_command))
    
    # Callback handler para botones
    application.add_handler(CallbackQueryHandler(button_callback))
    
    logger.info("Bot iniciado")
    print("=" * 60)
    print("BOT DE TELEGRAM INICIADO - @API_PF_VIU_bot")
    print("=" * 60)
    print(f"API: {API_BASE_URL}")
    print(f"Usuarios autorizados: {len(AUTHORIZED_USERS) if AUTHORIZED_USERS else 'Todos'}")
    print("\nComandos disponibles: 20+")
    print("Menus interactivos: SI")
    print("\nPresiona Ctrl+C para detener.")
    print("=" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
