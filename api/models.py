"""
Modelos de datos para la API Financiera
Define las estructuras de base de datos usando SQLAlchemy
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Customer(db.Model):
    """Modelo de cliente"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100))
    pais = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con transacciones
    transacciones = db.relationship('Transaction', backref='customer', lazy=True)
    # Relación con portfolio
    portfolio = db.relationship('Portfolio', backref='customer', lazy=True)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': f"{self.nombre} {self.apellido or ''}".strip(),
            'pais': self.pais,
            'telefono': self.telefono,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_transacciones': len(self.transacciones),
            'total_acciones': len(self.portfolio) if hasattr(self, 'portfolio') else 0
        }
    
    def __repr__(self):
        return f'<Customer {self.email}>'


class Transaction(db.Model):
    """Modelo de transacción"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    moneda = db.Column(db.String(3), default='USD')  # ISO 4217
    
    tipo = db.Column(db.String(20), nullable=False)  # payment, refund, transfer
    estado = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    
    descripcion = db.Column(db.String(255))
    referencia_externa = db.Column(db.String(100))  # ID de Stripe, PayPal, etc.
    
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_completado = db.Column(db.DateTime)
    
    extra_data = db.Column(db.JSON)  # Datos adicionales en formato JSON
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con auditoría
    audit_logs = db.relationship('AuditLog', backref='transaction', lazy=True)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_email': self.customer.email if self.customer else None,
            'customer_nombre': self.customer.nombre if self.customer else None,
            'monto': float(self.monto),
            'moneda': self.moneda,
            'tipo': self.tipo,
            'estado': self.estado,
            'descripcion': self.descripcion,
            'referencia_externa': self.referencia_externa,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None,
            'extra_data': self.extra_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.monto} {self.moneda}>'


class AuditLog(db.Model):
    """Modelo de registro de auditoría"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    
    accion = db.Column(db.String(50), nullable=False)  # created, updated, deleted
    usuario = db.Column(db.String(100))  # Email o ID del usuario que realizó la acción
    ip_address = db.Column(db.String(50))
    
    datos_anteriores = db.Column(db.JSON)  # Estado antes del cambio
    datos_nuevos = db.Column(db.JSON)  # Estado después del cambio
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'accion': self.accion,
            'usuario': self.usuario,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'datos_anteriores': self.datos_anteriores,
            'datos_nuevos': self.datos_nuevos
        }
    
    def __repr__(self):
        return f'<AuditLog {self.id}: {self.accion}>'


class Stock(db.Model):
    """Modelo de acción/stock"""
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    simbolo = db.Column(db.String(10), unique=True, nullable=False)  # AAPL, GOOGL, TSLA, etc.
    nombre = db.Column(db.String(200), nullable=False)  # Apple Inc., Google, Tesla, etc.
    sector = db.Column(db.String(100))  # Technology, Finance, Healthcare, etc.
    mercado = db.Column(db.String(50))  # NASDAQ, NYSE, etc.
    moneda = db.Column(db.String(3), default='USD')
    
    # Datos actuales (se actualizan periódicamente)
    precio_actual = db.Column(db.Numeric(10, 2))
    precio_apertura = db.Column(db.Numeric(10, 2))
    precio_cierre_anterior = db.Column(db.Numeric(10, 2))
    precio_max_dia = db.Column(db.Numeric(10, 2))
    precio_min_dia = db.Column(db.Numeric(10, 2))
    volumen = db.Column(db.BigInteger)
    
    # Cambios
    cambio_precio = db.Column(db.Numeric(10, 2))  # Cambio en valor absoluto
    cambio_porcentaje = db.Column(db.Numeric(5, 2))  # Cambio en porcentaje
    
    ultima_actualizacion = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con portfolio
    portfolios = db.relationship('Portfolio', backref='stock', lazy=True)
    
    def to_dict(self, include_market_data=True):
        """Convertir a diccionario para JSON"""
        base_dict = {
            'id': self.id,
            'simbolo': self.simbolo,
            'nombre': self.nombre,
            'sector': self.sector,
            'mercado': self.mercado,
            'moneda': self.moneda,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_market_data:
            base_dict.update({
                'precio_actual': float(self.precio_actual) if self.precio_actual else None,
                'precio_apertura': float(self.precio_apertura) if self.precio_apertura else None,
                'precio_cierre_anterior': float(self.precio_cierre_anterior) if self.precio_cierre_anterior else None,
                'precio_max_dia': float(self.precio_max_dia) if self.precio_max_dia else None,
                'precio_min_dia': float(self.precio_min_dia) if self.precio_min_dia else None,
                'volumen': int(self.volumen) if self.volumen else None,
                'cambio_precio': float(self.cambio_precio) if self.cambio_precio else None,
                'cambio_porcentaje': float(self.cambio_porcentaje) if self.cambio_porcentaje else None,
                'ultima_actualizacion': self.ultima_actualizacion.isoformat() if self.ultima_actualizacion else None
            })
        
        return base_dict
    
    def __repr__(self):
        return f'<Stock {self.simbolo}: {self.nombre}>'


class Portfolio(db.Model):
    """Modelo de cartera de acciones por cliente"""
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    
    # Información de la compra
    cantidad = db.Column(db.Integer, nullable=False)  # Número de acciones
    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)  # Precio al que se compraron
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Información adicional
    notas = db.Column(db.Text)  # Notas del cliente sobre la inversión
    activo = db.Column(db.Boolean, default=True)  # False si se vendió
    fecha_venta = db.Column(db.DateTime)
    precio_venta = db.Column(db.Numeric(10, 2))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calcular_valor_actual(self):
        """Calcular valor actual de la posición"""
        if self.stock and self.stock.precio_actual:
            return float(self.cantidad * self.stock.precio_actual)
        return None
    
    def calcular_ganancia_perdida(self):
        """Calcular ganancia o pérdida"""
        valor_actual = self.calcular_valor_actual()
        if valor_actual is not None:
            valor_compra = float(self.cantidad * self.precio_compra)
            return valor_actual - valor_compra
        return None
    
    def calcular_rendimiento_porcentaje(self):
        """Calcular rendimiento en porcentaje"""
        if self.stock and self.stock.precio_actual:
            return float(((self.stock.precio_actual - self.precio_compra) / self.precio_compra) * 100)
        return None
    
    def to_dict(self, include_stock_data=True):
        """Convertir a diccionario para JSON"""
        base_dict = {
            'id': self.id,
            'customer_id': self.customer_id,
            'stock_id': self.stock_id,
            'cantidad': self.cantidad,
            'precio_compra': float(self.precio_compra),
            'fecha_compra': self.fecha_compra.isoformat() if self.fecha_compra else None,
            'notas': self.notas,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # Incluir datos de la acción
        if include_stock_data and self.stock:
            base_dict['stock'] = {
                'simbolo': self.stock.simbolo,
                'nombre': self.stock.nombre,
                'precio_actual': float(self.stock.precio_actual) if self.stock.precio_actual else None,
                'moneda': self.stock.moneda
            }
        
        # Calcular métricas
        base_dict['valor_compra'] = float(self.cantidad * self.precio_compra)
        base_dict['valor_actual'] = self.calcular_valor_actual()
        base_dict['ganancia_perdida'] = self.calcular_ganancia_perdida()
        base_dict['rendimiento_porcentaje'] = self.calcular_rendimiento_porcentaje()
        
        if not self.activo and self.fecha_venta:
            base_dict['fecha_venta'] = self.fecha_venta.isoformat()
            base_dict['precio_venta'] = float(self.precio_venta) if self.precio_venta else None
        
        return base_dict
    
    def __repr__(self):
        return f'<Portfolio {self.id}: {self.cantidad} x {self.stock.simbolo if self.stock else "?"}>'


# Funciones auxiliares

def create_audit_log(transaction_id, accion, usuario='system', datos_anteriores=None, datos_nuevos=None):
    """Crear registro de auditoría"""
    from flask import request
    
    log = AuditLog(
        transaction_id=transaction_id,
        accion=accion,
        usuario=usuario,
        ip_address=request.remote_addr if request else None,
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos
    )
    
    db.session.add(log)
    return log
