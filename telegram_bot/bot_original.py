"""
Bot de Telegram para reportes de la API Financiera
Proporciona reportes y listas de transacciones
"""

import os
import logging
from datetime import datetime, timedelta
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
    
    # Crear teclado con botones
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
            InlineKeyboardButton("Estadisticas", callback_data='estadisticas'),
            InlineKeyboardButton("Ayuda", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
Hola {user.first_name}

Soy el bot de reportes de la API Financiera.

Selecciona una opcion del menu o usa los comandos:

**Comandos disponibles:**

**Reportes:**
- /reporte_diario - Transacciones del dia
- /reporte_semanal - Ultimos 7 dias
- /reporte_mensual - Mes actual

**Transacciones:**
- /listar_transacciones - Ultimas 10 transacciones
- /buscar_transaccion ID - Buscar por ID
- /transacciones_pendientes - Solo pendientes
- /transacciones_completadas - Solo completadas

**Clientes:**
- /cliente ID - Informacion de cliente
- /listar_clientes - Lista de clientes
- /top_clientes - Top 10 clientes

**Portfolio:**
- /portfolio - Reporte de portfolios
- /portfolio_cliente ID - Portfolio de un cliente
- /top_portfolios - Mejores portfolios

**Stocks:**
- /stocks - Lista de acciones disponibles
- /stock SIMBOLO - Informacion de una accion

**Utilidades:**
- /ping - Verificar conexion con API
- /menu - Mostrar menu interactivo

---
Usa /help para mas informacion.
    """
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


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
    
    elif query.data == 'estadisticas':
        await query.edit_message_text("Generando estadisticas...")
        await estadisticas_command_internal(query.message)
    
    elif query.data == 'help':
        await help_command_internal(query.message)
    
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
                InlineKeyboardButton("Estadisticas", callback_data='estadisticas'),
                InlineKeyboardButton("Ayuda", callback_data='help')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("**MENU PRINCIPAL**\n\nSelecciona una opcion:", reply_markup=reply_markup)
    
    # Comandos ejecutados desde botones
    elif query.data.startswith('cmd_'):
        command = query.data.replace('cmd_', '')
        await query.edit_message_text(f"Ejecutando {command}...")
        
        if command == 'reporte_diario':
            await reporte_diario_command_internal(query.message)
        elif command == 'reporte_semanal':
            await reporte_semanal_command_internal(query.message)
        elif command == 'reporte_mensual':
            await reporte_mensual_command_internal(query.message)
        elif command == 'listar_transacciones':
            await listar_transacciones_command_internal(query.message)
        elif command == 'transacciones_pendientes':
            await transacciones_pendientes_command_internal(query.message)
        elif command == 'transacciones_completadas':
            await transacciones_completadas_command_internal(query.message)
        elif command == 'listar_clientes':
            await listar_clientes_command_internal(query.message)
        elif command == 'top_clientes':
            await top_clientes_command_internal(query.message)
        elif command == 'portfolio':
            await portfolio_command_internal(query.message)
        elif command == 'top_portfolios':
            await top_portfolios_command_internal(query.message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
**Guia de uso del bot**

**REPORTES**
- /reporte_diario - Muestra todas las transacciones del dia actual con totales por estado
- /reporte_semanal - Transacciones de los ultimos 7 dias
- /reporte_mensual - Transacciones del mes en curso

**TRANSACCIONES**
- /listar_transacciones - Muestra las ultimas 10 transacciones
- /buscar_transaccion 123 - Busca la transaccion con ID 123

**CLIENTES**
- /cliente 5 - Muestra informacion del cliente con ID 5

**ESTADISTICAS**
- /estadisticas - Muestra un resumen general del sistema

**PORTFOLIO**
- /portfolio - Reporte consolidado de portfolios

---
**Ejemplos:**
- /buscar_transaccion 42
- /cliente 10
    """
    
    await update.message.reply_text(help_text)


async def estadisticas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /estadisticas - Estadisticas generales"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado para usar este bot.")
        return
    
    await update.message.reply_text("Generando estadisticas...")
    
    try:
        # Obtener datos de clientes
        customers_data = get_api('/customers?per_page=1000')
        if 'error' in customers_data:
            await update.message.reply_text(f"Error al obtener clientes: {customers_data['error']}")
            return
        
        # Obtener transacciones recientes
        transactions_data = get_api('/transactions?per_page=1000')
        if 'error' in transactions_data:
            await update.message.reply_text(f"Error al obtener transacciones: {transactions_data['error']}")
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
**ESTADISTICAS GENERALES**

**Clientes:**
- Total: {total_customers}

**Transacciones:**
- Total: {total_transactions}
- Completadas: {completed}
- Pendientes: {pending}
- Fallidas: {failed}

**Montos:**
- Total procesado: {format_money(total_amount)}
- Promedio: {format_money(total_amount/completed if completed > 0 else 0)}

Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en estadisticas_command: {e}")
        await update.message.reply_text(f"Error al generar estadisticas: {str(e)}")


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
**REPORTE DIARIO - {report.get('fecha', fecha_hoy)}**

**Totales:**
- Completadas: {format_money(report.get('total_completado', 0))}
- Pendientes: {format_money(report.get('total_pendiente', 0))}
- Fallidas: {format_money(report.get('total_fallido', 0))}

**Cantidad de transacciones:**
- Completadas: {report.get('count_completado', 0)}
- Pendientes: {report.get('count_pendiente', 0)}
- Fallidas: {report.get('count_fallido', 0)}
- TOTAL: {report.get('total_transacciones', 0)}

**Promedio:** {format_money(report.get('promedio_monto', 0))}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en reporte_diario: {e}")
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
- Completadas: {format_money(report.get('total_completado', 0))}
- Pendientes: {format_money(report.get('total_pendiente', 0))}
- Fallidas: {format_money(report.get('total_fallido', 0))}

**Total general:** {format_money(report.get('total_general', 0))}

**Transacciones:** {report.get('total_transacciones', 0)}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en reporte_semanal: {e}")
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
**REPORTE MENSUAL - {now.strftime('%B %Y')}**
{fecha_inicio} a {fecha_fin}

**Totales por estado:**
- Completadas: {format_money(report.get('total_completado', 0))}
- Pendientes: {format_money(report.get('total_pendiente', 0))}
- Fallidas: {format_money(report.get('total_fallido', 0))}

**Total general:** {format_money(report.get('total_general', 0))}

**Transacciones:** {report.get('total_transacciones', 0)}

**Promedio diario:** {format_money(report.get('total_general', 0) / now.day if now.day > 0 else 0)}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en reporte_mensual: {e}")
        await update.message.reply_text(f"Error: {str(e)}")


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
- Portfolios activos: {report.get('total_portfolios', 0)}
- Valor total: {format_money(report.get('valor_total', 0))}
- Total invertido: {format_money(report.get('total_invertido', 0))}
- Ganancia/Perdida: {format_money(report.get('ganancia_perdida_total', 0))}

**Top 5 portfolios:**
"""
        
        for i, portfolio in enumerate(portfolios[:5], 1):
            ganancia = portfolio.get('ganancia_perdida', 0)
            indicador = "[+]" if ganancia >= 0 else "[-]"
            message += f"\n{i}. {indicador} {portfolio.get('customer_nombre', 'N/A')}: {format_money(portfolio.get('valor_actual', 0))}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en portfolio: {e}")
        await update.message.reply_text(f"Error: {str(e)}")


async def listar_transacciones_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /listar_transacciones"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    await update.message.reply_text("Obteniendo ultimas transacciones...")
    
    try:
        data = get_api('/transactions?per_page=10&page=1')
        
        if 'error' in data:
            await update.message.reply_text(f"Error: {data['error']}")
            return
        
        transactions = data.get('data', [])
        
        if not transactions:
            await update.message.reply_text("No hay transacciones registradas.")
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
        logger.error(f"Error en listar_transacciones: {e}")
        await update.message.reply_text(f"Error: {str(e)}")


async def buscar_transaccion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar_transaccion ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    # Verificar que se proporciono un ID
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "Debes proporcionar un ID de transaccion.\n\n"
            "Ejemplo: /buscar_transaccion 42"
        )
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
            'completed': 'Completada',
            'pending': 'Pendiente',
            'failed': 'Fallida',
            'cancelled': 'Cancelada'
        }.get(trans['estado'], 'Desconocido')
        
        message = f"""
**TRANSACCION #{trans['id']}**

**Cliente:** {trans.get('customer_nombre', 'N/A')} ({trans.get('customer_email', 'N/A')})

**Monto:** {format_money(trans['monto'], trans['moneda'])}
**Tipo:** {trans['tipo']}
**Estado:** {estado_texto}

**Fecha:** {trans.get('fecha', 'N/A')}
**Completada:** {trans.get('fecha_completado', 'No completada')}

**Descripcion:** {trans.get('descripcion', 'Sin descripcion')}
**Referencia:** {trans.get('referencia_externa', 'N/A')}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en buscar_transaccion: {e}")
        await update.message.reply_text(f"Error: {str(e)}")


async def cliente_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /cliente ID"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("No estas autorizado.")
        return
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "Debes proporcionar un ID de cliente.\n\n"
            "Ejemplo: /cliente 5"
        )
        return
    
    customer_id = context.args[0]
    
    try:
        customer_id = int(customer_id)
    except ValueError:
        await update.message.reply_text("El ID debe ser un numero.")
        return
    
    await update.message.reply_text(f"Buscando cliente #{customer_id}...")
    
    try:
        # Obtener informacion del cliente
        customer_data = get_api(f'/customers/{customer_id}')
        
        if 'error' in customer_data:
            await update.message.reply_text(f"Cliente no encontrado: {customer_data['error']}")
            return
        
        customer = customer_data.get('data', {})
        
        # Obtener reporte del cliente
        report_data = get_api(f'/reports/customer/{customer_id}')
        report = report_data.get('data', {}) if 'data' in report_data else {}
        
        estado = "Activo" if customer.get('activo') else "Inactivo"
        
        message = f"""
**CLIENTE #{customer['id']}**

**Email:** {customer.get('email', 'N/A')}
**Nombre:** {customer.get('nombre_completo', 'N/A')}
**Pais:** {customer.get('pais', 'N/A')}
**Telefono:** {customer.get('telefono', 'N/A')}
**Estado:** {estado}

**Estadisticas:**
- Transacciones: {report.get('total_transacciones', 0)}
- Total gastado: {format_money(report.get('total_monto', 0))}
- Promedio: {format_money(report.get('promedio_monto', 0))}
- En portfolio: {customer.get('total_acciones', 0)} posiciones

**Registrado:** {customer.get('created_at', 'N/A')[:10]}
        """
        
        await update.message.reply_text(message)
        
    except Exception as e:
        logger.error(f"Error en cliente: {e}")
        await update.message.reply_text(f"Error: {str(e)}")


# ==================== MAIN ====================

def main():
    """Iniciar el bot"""
    
    # Verificar configuracion
    if not TELEGRAM_TOKEN:
        logger.error("ERROR: TELEGRAM_BOT_TOKEN no esta configurado en .env")
        print("\nERROR: TELEGRAM_BOT_TOKEN no esta configurado")
        print("Por favor, crea un archivo .env con tu token de Telegram")
        print("Ejemplo: TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrs...")
        return
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Registrar comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("estadisticas", estadisticas_command))
    application.add_handler(CommandHandler("reporte_diario", reporte_diario_command))
    application.add_handler(CommandHandler("reporte_semanal", reporte_semanal_command))
    application.add_handler(CommandHandler("reporte_mensual", reporte_mensual_command))
    application.add_handler(CommandHandler("portfolio", portfolio_command))
    application.add_handler(CommandHandler("listar_transacciones", listar_transacciones_command))
    application.add_handler(CommandHandler("buscar_transaccion", buscar_transaccion_command))
    application.add_handler(CommandHandler("cliente", cliente_command))
    
    # Iniciar bot
    logger.info("Bot iniciado correctamente")
    print("=" * 50)
    print("BOT DE TELEGRAM INICIADO")
    print("=" * 50)
    print(f"API: {API_BASE_URL}")
    print(f"Usuarios autorizados: {len(AUTHORIZED_USERS) if AUTHORIZED_USERS else 'Todos'}")
    print("\nEl bot esta ejecutandose. Presiona Ctrl+C para detener.")
    print("=" * 50)
    
    # Ejecutar bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
