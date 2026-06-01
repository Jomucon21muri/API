"""
Definición de endpoints REST de la API.

Este módulo contiene todos los endpoints de la API REST organizados
por categorías funcionales: clientes, transacciones, reportes, acciones,
portafolios y estadísticas del sistema.

Grupos de endpoints:
    - /api/customers: Gestión de clientes (4 endpoints)
    - /api/transactions: Gestión de transacciones (4 endpoints)
    - /api/reports: Generación de reportes (2 endpoints)
    - /api/stocks: Gestión de acciones del mercado (5 endpoints)
    - /api/portfolio: Gestión de portafolios (5 endpoints)
    - /api/stats: Estadísticas globales (1 endpoint)
    - /api/workflows: Estado de workflows (1 endpoint)
    - /api/health: Verificación de estado (1 endpoint)

Total: 23 endpoints disponibles
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func
from typing import Tuple, Dict, Any, List
import logging

from models import Customer, Transaction, AuditLog, Stock, Portfolio, create_audit_log

logger = logging.getLogger(__name__)


def register_routes(app: Flask, db: SQLAlchemy) -> None:
    """
    Registra todas las rutas en la aplicación Flask.
    
    Esta función define y registra todos los endpoints de la API REST.
    Se invoca durante la inicialización de la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
        db: Instancia de SQLAlchemy para acceso a base de datos
    """
    
    # ==================== CUSTOMERS ====================
    
    @app.route('/api/customers', methods=['GET'])
    def get_customers() -> Tuple[Dict[str, Any], int]:
        """
        Lista todos los clientes con filtros opcionales y paginación.
        
        Query Parameters:
            activo (bool): Filtrar por estado activo
            pais (str): Filtrar por código de país
            page (int): Número de página (default: 1)
            per_page (int): Registros por página (default: 50, max: 100)
            
        Returns:
            JSON con lista de clientes y metadatos de paginación
        """
        try:
            # Filtros opcionales
            activo = request.args.get('activo', type=bool)
            pais = request.args.get('pais')
            
            # Query base
            query = Customer.query
            
            if activo is not None:
                query = query.filter_by(activo=activo)
            
            if pais:
                query = query.filter_by(pais=pais)
            
            # Paginación con límite máximo
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 50, type=int), 100)
            
            customers = query.paginate(page=page, per_page=per_page, error_out=False)
            
            logger.info(f'Consulta de clientes: página {page}, filtros: activo={activo}, pais={pais}')
            
            return jsonify({
                'success': True,
                'data': [c.to_dict() for c in customers.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': customers.total,
                    'pages': customers.pages
                }
            }), 200
        
        except Exception as e:
            logger.error(f'Error al listar clientes: {e}', exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500
    
    
    @app.route('/api/customers/<int:customer_id>', methods=['GET'])
    def get_customer(customer_id: int) -> Tuple[Dict[str, Any], int]:
        """
        Obtiene los detalles de un cliente específico.
        
        Args:
            customer_id: ID del cliente a consultar
            
        Returns:
            JSON con datos del cliente o error 404 si no existe
        """
        customer = Customer.query.get_or_404(customer_id)
        logger.info(f'Consulta de cliente ID {customer_id}')
        return jsonify({
            'success': True,
            'data': customer.to_dict()
        }), 200
    
    
    @app.route('/api/customers', methods=['POST'])
    def create_customer() -> Tuple[Dict[str, Any], int]:
        """
        Crea un nuevo cliente en el sistema.
        
        Request Body (JSON):
            email (str, required): Correo electrónico único
            nombre (str, required): Nombre del cliente
            apellido (str, optional): Apellido del cliente
            pais (str, optional): Código de país (default: ES)
            telefono (str, optional): Número de teléfono
            
        Returns:
            JSON con datos del cliente creado (201) o error de validación (400)
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'success': False, 'error': 'Datos JSON requeridos'}), 400
            
            # Validaciones
            if not data.get('email'):
                return jsonify({'success': False, 'error': 'Email es requerido'}), 400
            
            if not data.get('nombre'):
                return jsonify({'success': False, 'error': 'Nombre es requerido'}), 400
            
            # Verificar email único
            if Customer.query.filter_by(email=data['email']).first():
                return jsonify({'success': False, 'error': 'Email ya existe'}), 400
            
            # Crear cliente
            customer = Customer(
                email=data['email'],
                nombre=data['nombre'],
                apellido=data.get('apellido'),
                pais=data.get('pais', 'ES'),
                telefono=data.get('telefono')
            )
            
            db.session.add(customer)
            db.session.commit()
            
            logger.info(f'Cliente creado: {customer.email} (ID: {customer.id})')
            
            return jsonify({
                'success': True,
                'message': 'Cliente creado exitosamente',
                'data': customer.to_dict()
            }), 201
        
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error al crear cliente: {e}', exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500
    
    
    # ==================== TRANSACTIONS ====================
    
    @app.route('/api/transactions', methods=['GET'])
    def get_transactions():
        """Listar transacciones con filtros"""
        try:
            # Filtros
            customer_id = request.args.get('customer_id', type=int)
            tipo = request.args.get('tipo')
            estado = request.args.get('estado')
            moneda = request.args.get('moneda')
            
            # Filtros de fecha
            fecha_desde = request.args.get('fecha_desde')
            fecha_hasta = request.args.get('fecha_hasta')
            
            # Filtros de monto
            monto_min = request.args.get('monto_min', type=float)
            monto_max = request.args.get('monto_max', type=float)
            
            # Query base
            query = Transaction.query
            
            # Aplicar filtros
            if customer_id:
                query = query.filter_by(customer_id=customer_id)
            
            if tipo:
                query = query.filter_by(tipo=tipo)
            
            if estado:
                query = query.filter_by(estado=estado)
            
            if moneda:
                query = query.filter_by(moneda=moneda)
            
            if fecha_desde:
                query = query.filter(Transaction.fecha >= datetime.fromisoformat(fecha_desde))
            
            if fecha_hasta:
                query = query.filter(Transaction.fecha <= datetime.fromisoformat(fecha_hasta))
            
            if monto_min:
                query = query.filter(Transaction.monto >= monto_min)
            
            if monto_max:
                query = query.filter(Transaction.monto <= monto_max)
            
            # Ordenar
            order_by = request.args.get('order_by', 'fecha')
            order_dir = request.args.get('order_dir', 'desc')
            
            if order_dir == 'desc':
                query = query.order_by(getattr(Transaction, order_by).desc())
            else:
                query = query.order_by(getattr(Transaction, order_by).asc())
            
            # Paginación
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            
            transactions = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'success': True,
                'data': [t.to_dict() for t in transactions.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': transactions.total,
                    'pages': transactions.pages
                }
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/transactions/<int:transaction_id>', methods=['GET'])
    def get_transaction(transaction_id):
        """Obtener una transacción específica"""
        transaction = Transaction.query.get_or_404(transaction_id)
        return jsonify({
            'success': True,
            'data': transaction.to_dict()
        })
    
    
    @app.route('/api/transactions', methods=['POST'])
    def create_transaction():
        """Crear nueva transacción"""
        try:
            data = request.get_json()
            
            # Validaciones
            if not data.get('customer_id'):
                return jsonify({'error': 'customer_id es requerido'}), 400
            
            if not data.get('monto'):
                return jsonify({'error': 'monto es requerido'}), 400
            
            if not data.get('tipo'):
                return jsonify({'error': 'tipo es requerido'}), 400
            
            # Verificar que el cliente existe
            customer = Customer.query.get(data['customer_id'])
            if not customer:
                return jsonify({'error': 'Cliente no encontrado'}), 404
            
            # Crear transacción
            transaction = Transaction(
                customer_id=data['customer_id'],
                monto=data['monto'],
                moneda=data.get('moneda', 'USD'),
                tipo=data['tipo'],
                estado=data.get('estado', 'pending'),
                descripcion=data.get('descripcion'),
                referencia_externa=data.get('referencia_externa'),
                metadata=data.get('metadata')
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            # Crear log de auditoría
            create_audit_log(
                transaction_id=transaction.id,
                accion='created',
                datos_nuevos=transaction.to_dict()
            )
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Transacción creada exitosamente',
                'data': transaction.to_dict()
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/transactions/<int:transaction_id>', methods=['PATCH'])
    def update_transaction(transaction_id):
        """Actualizar estado de transacción"""
        try:
            transaction = Transaction.query.get_or_404(transaction_id)
            data = request.get_json()
            
            # Guardar datos anteriores para auditoría
            datos_anteriores = transaction.to_dict()
            
            # Actualizar campos permitidos
            if 'estado' in data:
                transaction.estado = data['estado']
                
                if data['estado'] == 'completed':
                    transaction.fecha_completado = datetime.utcnow()
            
            if 'descripcion' in data:
                transaction.descripcion = data['descripcion']
            
            if 'metadata' in data:
                transaction.metadata = data['metadata']
            
            db.session.commit()
            
            # Crear log de auditoría
            create_audit_log(
                transaction_id=transaction.id,
                accion='updated',
                datos_anteriores=datos_anteriores,
                datos_nuevos=transaction.to_dict()
            )
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Transacción actualizada',
                'data': transaction.to_dict()
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    
    # ==================== REPORTS ====================
    
    @app.route('/api/reports/daily', methods=['GET'])
    def daily_report():
        """Reporte de transacciones del día"""
        try:
            # Fecha objetivo (hoy por defecto)
            fecha_str = request.args.get('fecha')
            if fecha_str:
                fecha = datetime.fromisoformat(fecha_str).date()
            else:
                fecha = datetime.utcnow().date()
            
            # Inicio y fin del día
            inicio_dia = datetime.combine(fecha, datetime.min.time())
            fin_dia = datetime.combine(fecha, datetime.max.time())
            
            # Obtener transacciones del día
            transacciones = Transaction.query.filter(
                Transaction.fecha >= inicio_dia,
                Transaction.fecha <= fin_dia
            ).all()
            
            # Calcular estadísticas
            total_transacciones = len(transacciones)
            
            if total_transacciones == 0:
                return jsonify({
                    'success': True,
                    'fecha': fecha.isoformat(),
                    'total_transacciones': 0,
                    'monto_total': 0,
                    'monto_promedio': 0
                })
            
            montos = [float(t.monto) for t in transacciones]
            monto_total = sum(montos)
            monto_promedio = monto_total / total_transacciones
            
            # Agrupar por tipo
            por_tipo = {}
            for t in transacciones:
                if t.tipo not in por_tipo:
                    por_tipo[t.tipo] = {'count': 0, 'total': 0}
                por_tipo[t.tipo]['count'] += 1
                por_tipo[t.tipo]['total'] += float(t.monto)
            
            # Agrupar por estado
            por_estado = {}
            for t in transacciones:
                if t.estado not in por_estado:
                    por_estado[t.estado] = 0
                por_estado[t.estado] += 1
            
            return jsonify({
                'success': True,
                'fecha': fecha.isoformat(),
                'total_transacciones': total_transacciones,
                'monto_total': round(monto_total, 2),
                'monto_promedio': round(monto_promedio, 2),
                'transaccion_minima': round(min(montos), 2),
                'transaccion_maxima': round(max(montos), 2),
                'por_tipo': por_tipo,
                'por_estado': por_estado,
                'clientes_unicos': len(set(t.customer_id for t in transacciones))
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/reports/customer/<int:customer_id>', methods=['GET'])
    def customer_report(customer_id):
        """Reporte de un cliente específico"""
        try:
            customer = Customer.query.get_or_404(customer_id)
            
            transacciones = Transaction.query.filter_by(customer_id=customer_id).all()
            
            if not transacciones:
                return jsonify({
                    'success': True,
                    'customer': customer.to_dict(),
                    'total_transacciones': 0,
                    'gasto_total': 0
                })
            
            montos = [float(t.monto) for t in transacciones]
            
            return jsonify({
                'success': True,
                'customer': customer.to_dict(),
                'total_transacciones': len(transacciones),
                'gasto_total': round(sum(montos), 2),
                'gasto_promedio': round(sum(montos) / len(montos), 2),
                'primera_transaccion': min(t.fecha for t in transacciones).isoformat(),
                'ultima_transaccion': max(t.fecha for t in transacciones).isoformat()
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    # ==================== UTILITY ENDPOINTS ====================
    
    @app.route('/api/exchange-rate/<string:currency>', methods=['GET'])
    def get_exchange_rate(currency):
        """Obtener tipo de cambio (simulado o API externa)"""
        # En producción, usar API real como exchangerate-api.com
        
        # Tasas simuladas
        rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'GBP': 0.79,
            'JPY': 149.50,
            'MXN': 17.20
        }
        
        currency = currency.upper()
        
        if currency not in rates:
            return jsonify({'error': 'Moneda no soportada'}), 400
        
        return jsonify({
            'success': True,
            'base': 'USD',
            'currency': currency,
            'rate': rates[currency],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    
    # ==================== STOCKS & PORTFOLIO ====================
    
    @app.route('/api/stocks', methods=['GET'])
    def get_stocks():
        """Listar todas las acciones disponibles"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            sector = request.args.get('sector')
            
            query = Stock.query.filter_by(activo=True)
            
            if sector:
                query = query.filter_by(sector=sector)
            
            stocks = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'success': True,
                'data': [s.to_dict() for s in stocks.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': stocks.total,
                    'pages': stocks.pages
                }
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/stocks/<string:simbolo>', methods=['GET'])
    def get_stock(simbolo):
        """Obtener información de una acción específica"""
        try:
            from stock_service import StockService
            
            # Buscar en BD
            stock = Stock.query.filter_by(simbolo=simbolo.upper()).first()
            
            # Si no existe o está desactualizada, obtener de API
            actualizar = request.args.get('actualizar', 'false').lower() == 'true'
            
            if not stock or actualizar:
                stock = StockService.actualizar_precio(simbolo)
                if not stock:
                    return jsonify({'error': 'Acción no encontrada'}), 404
            
            return jsonify({
                'success': True,
                'data': stock.to_dict()
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/stocks/<string:simbolo>/historico', methods=['GET'])
    def get_stock_historico(simbolo):
        """Obtener datos históricos de una acción"""
        try:
            from stock_service import StockService
            
            periodo = request.args.get('periodo', '1mo')
            datos = StockService.obtener_historico(simbolo, periodo)
            
            if datos is None:
                return jsonify({'error': 'No se pudieron obtener datos históricos'}), 404
            
            return jsonify({
                'success': True,
                'simbolo': simbolo.upper(),
                'periodo': periodo,
                'data': datos
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/stocks/populares', methods=['GET'])
    def get_stocks_populares():
        """Obtener acciones más populares con precios actualizados"""
        try:
            # Lista de símbolos populares
            simbolos_populares = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
                                'META', 'NVDA', 'JPM', 'V', 'WMT', 
                                'NFLX', 'DIS', 'PYPL', 'INTC', 'AMD']
            
            # Obtener de la base de datos
            stocks = Stock.query.filter(Stock.simbolo.in_(simbolos_populares)).all()
            
            # Si se solicita actualización en tiempo real
            actualizar = request.args.get('refresh', 'false').lower() == 'true'
            
            if actualizar:
                from stock_service import StockService
                # Actualizar precios en background
                for stock in stocks:
                    try:
                        StockService.actualizar_precio(stock.simbolo)
                    except:
                        pass  # Continuar aunque falle alguna actualización
                
                # Recargar stocks actualizados
                stocks = Stock.query.filter(Stock.simbolo.in_(simbolos_populares)).all()
            
            return jsonify({
                'success': True,
                'data': [stock.to_dict(include_market_data=True) for stock in stocks]
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/stocks/actualizar-multiples', methods=['POST'])
    def actualizar_multiples_stocks():
        """Actualizar precios de múltiples acciones"""
        try:
            from stock_service import StockService
            
            data = request.get_json()
            simbolos = data.get('simbolos', [])
            
            if not simbolos:
                return jsonify({'error': 'Se requiere lista de símbolos'}), 400
            
            resultados = []
            for simbolo in simbolos:
                stock = StockService.actualizar_precio(simbolo)
                if stock:
                    resultados.append(stock.to_dict())
            
            return jsonify({
                'success': True,
                'data': resultados,
                'total_actualizados': len(resultados)
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/portfolio', methods=['GET'])
    def get_all_portfolios():
        """Listar todas las posiciones de cartera"""
        try:
            customer_id = request.args.get('customer_id', type=int)
            activo = request.args.get('activo', 'true').lower() == 'true'
            
            query = Portfolio.query
            
            if customer_id:
                query = query.filter_by(customer_id=customer_id)
            
            if activo:
                query = query.filter_by(activo=True)
            
            portfolios = query.all()
            
            # Calcular totales
            valor_total = sum([p.calcular_valor_actual() or 0 for p in portfolios])
            ganancia_total = sum([p.calcular_ganancia_perdida() or 0 for p in portfolios])
            
            return jsonify({
                'success': True,
                'data': [p.to_dict() for p in portfolios],
                'resumen': {
                    'total_posiciones': len(portfolios),
                    'valor_total': valor_total,
                    'ganancia_total': ganancia_total,
                    'rendimiento_porcentaje': (ganancia_total / (valor_total - ganancia_total) * 100) if valor_total > ganancia_total else 0
                }
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/portfolio/customer/<int:customer_id>', methods=['GET'])
    def get_customer_portfolio(customer_id):
        """Obtener cartera completa de un cliente"""
        try:
            customer = Customer.query.get_or_404(customer_id)
            portfolios = Portfolio.query.filter_by(customer_id=customer_id, activo=True).all()
            
            # Actualizar precios de todas las acciones
            from stock_service import StockService
            simbolos = list(set([p.stock.simbolo for p in portfolios if p.stock]))
            
            if simbolos:
                for simbolo in simbolos:
                    StockService.actualizar_precio(simbolo)
            
            # Calcular métricas
            valor_total_actual = sum([p.calcular_valor_actual() or 0 for p in portfolios])
            valor_total_compra = sum([float(p.cantidad * p.precio_compra) for p in portfolios])
            ganancia_total = valor_total_actual - valor_total_compra
            rendimiento = (ganancia_total / valor_total_compra * 100) if valor_total_compra > 0 else 0
            
            return jsonify({
                'success': True,
                'customer': {
                    'id': customer.id,
                    'nombre_completo': customer.nombre + ' ' + (customer.apellido or ''),
                    'email': customer.email
                },
                'portfolio': [p.to_dict() for p in portfolios],
                'resumen': {
                    'total_posiciones': len(portfolios),
                    'valor_compra': valor_total_compra,
                    'valor_actual': valor_total_actual,
                    'ganancia_perdida': ganancia_total,
                    'rendimiento_porcentaje': rendimiento
                }
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/portfolio', methods=['POST'])
    def create_portfolio_position():
        """Crear nueva posición en cartera (comprar acciones)"""
        try:
            data = request.get_json()
            
            # Validaciones
            if not data.get('customer_id'):
                return jsonify({'error': 'customer_id es requerido'}), 400
            
            if not data.get('simbolo'):
                return jsonify({'error': 'simbolo es requerido'}), 400
            
            if not data.get('cantidad') or data['cantidad'] <= 0:
                return jsonify({'error': 'cantidad debe ser mayor a 0'}), 400
            
            # Verificar cliente existe
            customer = Customer.query.get(data['customer_id'])
            if not customer:
                return jsonify({'error': 'Cliente no encontrado'}), 404
            
            # Obtener o crear acción
            from stock_service import StockService
            stock = Stock.query.filter_by(simbolo=data['simbolo'].upper()).first()
            
            if not stock:
                stock = StockService.actualizar_precio(data['simbolo'])
                if not stock:
                    return jsonify({'error': 'No se pudo obtener información de la acción'}), 404
            else:
                # Actualizar precio
                StockService.actualizar_precio(data['simbolo'])
                stock = Stock.query.filter_by(simbolo=data['simbolo'].upper()).first()
            
            # Usar precio actual o precio especificado
            precio_compra = data.get('precio_compra', stock.precio_actual)
            
            # Crear posición
            portfolio = Portfolio(
                customer_id=data['customer_id'],
                stock_id=stock.id,
                cantidad=data['cantidad'],
                precio_compra=precio_compra,
                notas=data.get('notas')
            )
            
            db.session.add(portfolio)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Posición creada exitosamente',
                'data': portfolio.to_dict()
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/portfolio/<int:portfolio_id>', methods=['DELETE'])
    def sell_portfolio_position(portfolio_id):
        """Vender posición (marcar como inactiva)"""
        try:
            portfolio = Portfolio.query.get_or_404(portfolio_id)
            
            if not portfolio.activo:
                return jsonify({'error': 'La posición ya fue vendida'}), 400
            
            data = request.get_json() or {}
            
            # Actualizar precio actual de la acción
            from stock_service import StockService
            StockService.actualizar_precio(portfolio.stock.simbolo)
            
            # Usar precio actual o precio especificado
            precio_venta = data.get('precio_venta', portfolio.stock.precio_actual)
            
            portfolio.activo = False
            portfolio.fecha_venta = datetime.utcnow()
            portfolio.precio_venta = precio_venta
            
            db.session.commit()
            
            # Calcular ganancia/pérdida
            valor_compra = float(portfolio.cantidad * portfolio.precio_compra)
            valor_venta = float(portfolio.cantidad * precio_venta)
            ganancia = valor_venta - valor_compra
            
            return jsonify({
                'success': True,
                'message': 'Posición vendida exitosamente',
                'data': portfolio.to_dict(),
                'transaccion': {
                    'valor_compra': valor_compra,
                    'valor_venta': valor_venta,
                    'ganancia_perdida': ganancia,
                    'rendimiento_porcentaje': (ganancia / valor_compra * 100) if valor_compra > 0 else 0
                }
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/portfolio/<int:portfolio_id>', methods=['PATCH'])
    def update_portfolio_position(portfolio_id):
        """Actualizar posición (modificar cantidad o notas)"""
        try:
            portfolio = Portfolio.query.get_or_404(portfolio_id)
            data = request.get_json()
            
            if 'cantidad' in data:
                if data['cantidad'] <= 0:
                    return jsonify({'error': 'cantidad debe ser mayor a 0'}), 400
                portfolio.cantidad = data['cantidad']
            
            if 'notas' in data:
                portfolio.notas = data['notas']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Posición actualizada exitosamente',
                'data': portfolio.to_dict()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/stats/global', methods=['GET'])
    def get_global_stats():
        """Obtener estadísticas globales del sistema"""
        try:
            # Clientes
            total_customers = Customer.query.count()
            active_customers = Customer.query.filter_by(activo=True).count()
            
            # Agrupar clientes por país
            countries_stats = db.session.query(
                Customer.pais,
                func.count(Customer.id).label('count')
            ).group_by(Customer.pais).all()
            
            countries = [{'pais': pais, 'total': count} for pais, count in countries_stats]
            
            # Transacciones
            total_transactions = Transaction.query.count()
            completed_transactions = Transaction.query.filter_by(estado='completed').count()
            pending_transactions = Transaction.query.filter_by(estado='pending').count()
            
            # Volumen de transacciones por moneda
            transaction_volume = db.session.query(
                Transaction.moneda,
                func.sum(Transaction.monto).label('total'),
                func.count(Transaction.id).label('count')
            ).filter_by(estado='completed').group_by(Transaction.moneda).all()
            
            volumes = [{'moneda': moneda, 'total': float(total), 'transacciones': count} 
                      for moneda, total, count in transaction_volume]
            
            # Portfolio
            total_portfolios = Portfolio.query.filter_by(activo=True).count()
            customers_with_portfolio = db.session.query(
                Portfolio.customer_id
            ).filter_by(activo=True).distinct().count()
            
            # Acciones más populares en portfolios
            popular_stocks = db.session.query(
                Stock.simbolo,
                Stock.nombre,
                func.count(Portfolio.id).label('inversores'),
                func.sum(Portfolio.cantidad).label('total_acciones')
            ).join(Portfolio).filter(Portfolio.activo == True).group_by(
                Stock.simbolo, Stock.nombre
            ).order_by(func.count(Portfolio.id).desc()).limit(10).all()
            
            top_stocks = [{
                'simbolo': simbolo,
                'nombre': nombre,
                'inversores': inv,
                'total_acciones': int(total)
            } for simbolo, nombre, inv, total in popular_stocks]
            
            # Stocks disponibles
            total_stocks = Stock.query.count()
            
            return jsonify({
                'success': True,
                'data': {
                    'clientes': {
                        'total': total_customers,
                        'activos': active_customers,
                        'por_pais': countries,
                        'promedio_transacciones': round(total_transactions / max(total_customers, 1), 1)
                    },
                    'transacciones': {
                        'total': total_transactions,
                        'completadas': completed_transactions,
                        'pendientes': pending_transactions,
                        'volumen_por_moneda': volumes
                    },
                    'portfolios': {
                        'posiciones_activas': total_portfolios,
                        'clientes_con_portfolio': customers_with_portfolio,
                        'promedio_posiciones': round(total_portfolios / max(customers_with_portfolio, 1), 1),
                        'acciones_mas_populares': top_stocks
                    },
                    'mercado': {
                        'acciones_disponibles': total_stocks
                    }
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/workflows', methods=['GET'])
    def get_workflows():
        """Obtener workflows de n8n, Make y Zapier"""
        try:
            import os
            from pathlib import Path
            from workflow_service import get_workflows_summary
            
            # Obtener ruta base del proyecto (un nivel arriba de api/)
            base_path = Path(__file__).parent.parent
            
            summary = get_workflows_summary(base_path)
            
            return jsonify({
                'success': True,
                'data': summary
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/reports/clientes', methods=['GET'])
    def report_clientes():
        """Reporte de clientes por país y estado"""
        try:
            # Agrupar clientes por país
            clientes_por_pais = db.session.query(
                Customer.pais,
                func.count(Customer.id).label('total'),
                func.sum(func.cast(Customer.activo, db.Integer)).label('activos')
            ).group_by(Customer.pais).all()
            
            # Clientes recientes (últimos 30 días)
            desde = datetime.now() - timedelta(days=30)
            clientes_recientes = Customer.query.filter(
                Customer.created_at >= desde
            ).count()
            
            return jsonify({
                'success': True,
                'data': {
                    'por_pais': [{
                        'pais': pais,
                        'total': total,
                        'activos': activos or 0
                    } for pais, total, activos in clientes_por_pais],
                    'nuevos_ultimos_30_dias': clientes_recientes,
                    'total_general': Customer.query.count(),
                    'activos_general': Customer.query.filter_by(activo=True).count()
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/reports/transacciones', methods=['GET'])
    def report_transacciones():
        """Reporte de transacciones por período"""
        try:
            # Parámetros de fecha
            dias = request.args.get('dias', 30, type=int)
            desde = datetime.now() - timedelta(days=dias)
            
            # Transacciones por estado
            por_estado = db.session.query(
                Transaction.estado,
                func.count(Transaction.id).label('total'),
                func.sum(Transaction.monto).label('volumen')
            ).filter(Transaction.fecha >= desde).group_by(Transaction.estado).all()
            
            # Transacciones por tipo
            por_tipo = db.session.query(
                Transaction.tipo,
                func.count(Transaction.id).label('total'),
                func.sum(Transaction.monto).label('volumen')
            ).filter(Transaction.fecha >= desde).group_by(Transaction.tipo).all()
            
            # Transacciones por moneda
            por_moneda = db.session.query(
                Transaction.moneda,
                func.count(Transaction.id).label('total'),
                func.sum(Transaction.monto).label('volumen')
            ).filter(Transaction.fecha >= desde).group_by(Transaction.moneda).all()
            
            # Transacciones por día (últimos 30 días)
            transacciones_diarias = db.session.query(
                func.date(Transaction.fecha).label('fecha'),
                func.count(Transaction.id).label('total'),
                func.sum(Transaction.monto).label('volumen')
            ).filter(Transaction.fecha >= desde).group_by(
                func.date(Transaction.fecha)
            ).order_by(func.date(Transaction.fecha)).all()
            
            return jsonify({
                'success': True,
                'data': {
                    'periodo_dias': dias,
                    'por_estado': [{
                        'estado': estado,
                        'total': total,
                        'volumen': float(volumen or 0)
                    } for estado, total, volumen in por_estado],
                    'por_tipo': [{
                        'tipo': tipo,
                        'total': total,
                        'volumen': float(volumen or 0)
                    } for tipo, total, volumen in por_tipo],
                    'por_moneda': [{
                        'moneda': moneda,
                        'total': total,
                        'volumen': float(volumen or 0)
                    } for moneda, total, volumen in por_moneda],
                    'diarias': [{
                        'fecha': str(fecha) if fecha else '',
                        'total': total,
                        'volumen': float(volumen or 0)
                    } for fecha, total, volumen in transacciones_diarias]
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/reports/portfolio', methods=['GET'])
    def report_portfolio():
        """Reporte consolidado de portfolios"""
        try:
            # Valor total del mercado (todas las posiciones)
            portfolios_activos = Portfolio.query.filter_by(activo=True).all()
            
            valor_total = 0
            ganancia_total = 0
            costo_total = 0
            
            for p in portfolios_activos:
                if p.stock and p.stock.precio_actual:
                    valor_total += p.calcular_valor_actual()
                    ganancia_total += p.calcular_ganancia_perdida()
                    costo_total += p.precio_compra * p.cantidad
            
            # Top ganadores y perdedores
            posiciones_con_rendimiento = []
            for p in portfolios_activos:
                if p.stock and p.stock.precio_actual:
                    rendimiento = p.calcular_rendimiento_porcentaje()
                    customer_name = 'Desconocido'
                    if p.customer:
                        customer_name = f"{p.customer.nombre} {p.customer.apellido or ''}".strip()
                    
                    posiciones_con_rendimiento.append({
                        'customer_id': p.customer_id,
                        'customer_nombre': customer_name,
                        'simbolo': p.stock.simbolo,
                        'nombre': p.stock.nombre,
                        'cantidad': p.cantidad,
                        'valor_actual': p.calcular_valor_actual(),
                        'ganancia': p.calcular_ganancia_perdida(),
                        'rendimiento': rendimiento
                    })
            
            # Ordenar por rendimiento
            posiciones_con_rendimiento.sort(key=lambda x: x['rendimiento'], reverse=True)
            
            return jsonify({
                'success': True,
                'data': {
                    'resumen': {
                        'valor_total_mercado': round(valor_total, 2),
                        'ganancia_total': round(ganancia_total, 2),
                        'costo_total': round(costo_total, 2),
                        'rendimiento_promedio': round((float(ganancia_total) / float(costo_total) * 100) if costo_total > 0 else 0, 2),
                        'total_posiciones': len(portfolios_activos),
                        'total_clientes': db.session.query(Portfolio.customer_id).filter_by(activo=True).distinct().count()
                    },
                    'top_ganadores': posiciones_con_rendimiento[:10],
                    'top_perdedores': posiciones_con_rendimiento[-10:]
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/export/customers', methods=['GET'])
    def export_customers_csv():
        """Exportar clientes a CSV"""
        try:
            import io
            import csv
            from flask import make_response
            
            customers = Customer.query.all()
            
            # Crear CSV en memoria
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow(['ID', 'Nombre', 'Apellido', 'Email', 'Teléfono', 'País', 'Activo', 'Fecha Registro'])
            
            # Datos
            for c in customers:
                writer.writerow([
                    c.id,
                    c.nombre,
                    c.apellido or '',
                    c.email,
                    c.telefono or '',
                    c.pais or '',
                    'Sí' if c.activo else 'No',
                    c.created_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename=clientes.csv'
            
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/export/transactions', methods=['GET'])
    def export_transactions_csv():
        """Exportar transacciones a CSV"""
        try:
            import io
            import csv
            from flask import make_response
            
            transactions = Transaction.query.order_by(Transaction.fecha.desc()).limit(1000).all()
            
            # Crear CSV en memoria
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow(['ID', 'Cliente ID', 'Cliente Nombre', 'Monto', 'Moneda', 'Tipo', 'Estado', 'Descripción', 'Fecha'])
            
            # Datos
            for t in transactions:
                customer_name = ''
                if t.customer:
                    customer_name = f"{t.customer.nombre} {t.customer.apellido or ''}".strip()
                    
                writer.writerow([
                    t.id,
                    t.customer_id,
                    customer_name,
                    t.monto,
                    t.moneda,
                    t.tipo,
                    t.estado,
                    t.descripcion or '',
                    t.fecha.strftime('%Y-%m-%d %H:%M:%S')
                ])
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv; charset=utf-8'
            response.headers['Content-Disposition'] = 'attachment; filename=transacciones.csv'
            
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/portfolio/analisis/<int:customer_id>', methods=['GET'])
    def portfolio_analisis(customer_id):
        """Análisis avanzado de portfolio de un cliente"""
        try:
            customer = Customer.query.get_or_404(customer_id)
            portfolios = Portfolio.query.filter_by(
                customer_id=customer_id,
                activo=True
            ).all()
            
            if not portfolios:
                return jsonify({
                    'success': True,
                    'data': {
                        'diversificacion': {},
                        'riesgo': {},
                        'rendimiento': {},
                        'recomendaciones': ['No hay posiciones en el portfolio']
                    }
                })
            
            # Calcular métricas
            valor_total = sum(p.calcular_valor_actual() for p in portfolios if p.stock and p.stock.precio_actual)
            costo_total = sum(float(p.precio_compra) * p.cantidad for p in portfolios)
            ganancia_total = sum(p.calcular_ganancia_perdida() for p in portfolios if p.stock and p.stock.precio_actual)
            
            # Diversificación por sector
            sectores = {}
            for p in portfolios:
                if p.stock:
                    sector = p.stock.sector or 'Otros'
                    valor = p.calcular_valor_actual() if p.stock.precio_actual else 0
                    sectores[sector] = sectores.get(sector, 0) + valor
            
            # Concentración (% en top 3 posiciones)
            valores_posiciones = sorted(
                [p.calcular_valor_actual() for p in portfolios if p.stock and p.stock.precio_actual],
                reverse=True
            )
            concentracion_top3 = (float(sum(valores_posiciones[:3])) / float(valor_total) * 100) if valor_total > 0 else 0
            
            # Volatilidad aproximada (basada en cambio porcentual diario)
            volatilidad_promedio = 0
            count_vol = 0
            for p in portfolios:
                if p.stock and p.stock.cambio_porcentaje is not None:
                    volatilidad_promedio += abs(float(p.stock.cambio_porcentaje))
                    count_vol += 1
            volatilidad_promedio = volatilidad_promedio / count_vol if count_vol > 0 else 0
            
            # Recomendaciones
            recomendaciones = []
            if concentracion_top3 > 50:
                recomendaciones.append('Alta concentración: considera diversificar más tu portfolio')
            if len(sectores) < 3:
                recomendaciones.append('Pocos sectores: diversifica en diferentes industrias')
            if volatilidad_promedio > 5:
                recomendaciones.append('Alta volatilidad: considera equilibrar con acciones más estables')
            if ganancia_total < 0:
                recomendaciones.append('Portfolio en pérdidas: revisa estrategia o espera recuperación')
            if not recomendaciones:
                recomendaciones.append('Portfolio bien equilibrado. Mantén la diversificación')
            
            return jsonify({
                'success': True,
                'data': {
                    'diversificacion': {
                        'sectores': sectores,
                        'num_sectores': len(sectores),
                        'concentracion_top3': round(concentracion_top3, 2)
                    },
                    'riesgo': {
                        'volatilidad_promedio': round(volatilidad_promedio, 2),
                        'nivel': 'Alto' if volatilidad_promedio > 5 else ('Medio' if volatilidad_promedio > 2 else 'Bajo')
                    },
                    'rendimiento': {
                        'valor_total': round(valor_total, 2),
                        'costo_total': round(costo_total, 2),
                        'ganancia_total': round(ganancia_total, 2),
                        'rendimiento_porcentaje': round((float(ganancia_total) / float(costo_total) * 100) if costo_total > 0 else 0, 2)
                    },
                    'recomendaciones': recomendaciones
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500


