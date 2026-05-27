"""
Script para actualizar la base de datos con tablas de stocks y portfolio
Ejecutar desde el directorio api: python update_db_stocks.py
"""

from app import app, db
from models import Customer, Stock, Portfolio
from datetime import datetime, timedelta
import random

def actualizar_tablas():
    """Crear las nuevas tablas"""
    with app.app_context():
        print("Creando nuevas tablas para stocks y portfolio...")
        db.create_all()
        print("✓ Tablas actualizadas exitosamente")

def agregar_stocks_ejemplo():
    """Agregar stocks de ejemplo"""
    with app.app_context():
        existing_stocks = Stock.query.all()
        if existing_stocks:
            print(f"⚠ Ya existen {len(existing_stocks)} stocks en la base de datos")
            # Devolver los IDs de los stocks existentes
            return [s.id for s in existing_stocks]
        
        print("Agregando stocks de ejemplo...")
        
        stocks_data = [
            {'simbolo': 'AAPL', 'nombre': 'Apple Inc.', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 178.25},
            {'simbolo': 'MSFT', 'nombre': 'Microsoft Corporation', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 415.50},
            {'simbolo': 'GOOGL', 'nombre': 'Alphabet Inc.', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 140.75},
            {'simbolo': 'AMZN', 'nombre': 'Amazon.com Inc.', 'sector': 'Consumer Cyclical', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 175.30},
            {'simbolo': 'TSLA', 'nombre': 'Tesla Inc.', 'sector': 'Automotive', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 242.15},
            {'simbolo': 'META', 'nombre': 'Meta Platforms Inc.', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 485.90},
            {'simbolo': 'NVDA', 'nombre': 'NVIDIA Corporation', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 875.20},
            {'simbolo': 'JPM', 'nombre': 'JPMorgan Chase & Co.', 'sector': 'Financial Services', 'mercado': 'NYSE', 'moneda': 'USD', 'precio_actual': 195.45},
            {'simbolo': 'V', 'nombre': 'Visa Inc.', 'sector': 'Financial Services', 'mercado': 'NYSE', 'moneda': 'USD', 'precio_actual': 280.60},
            {'simbolo': 'WMT', 'nombre': 'Walmart Inc.', 'sector': 'Consumer Defensive', 'mercado': 'NYSE', 'moneda': 'USD', 'precio_actual': 165.80},
            {'simbolo': 'DIS', 'nombre': 'The Walt Disney Company', 'sector': 'Communication Services', 'mercado': 'NYSE', 'moneda': 'USD', 'precio_actual': 112.35},
            {'simbolo': 'NFLX', 'nombre': 'Netflix Inc.', 'sector': 'Communication Services', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 625.50},
            {'simbolo': 'PYPL', 'nombre': 'PayPal Holdings Inc.', 'sector': 'Financial Services', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 65.40},
            {'simbolo': 'INTC', 'nombre': 'Intel Corporation', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 42.75},
            {'simbolo': 'AMD', 'nombre': 'Advanced Micro Devices Inc.', 'sector': 'Technology', 'mercado': 'NASDAQ', 'moneda': 'USD', 'precio_actual': 165.30},
        ]
        
        stocks = []
        for data in stocks_data:
            stock = Stock(**data)
            # Simular datos de mercado
            stock.precio_apertura = data['precio_actual'] * random.uniform(0.98, 1.02)
            stock.precio_cierre_anterior = data['precio_actual'] * random.uniform(0.95, 1.05)
            stock.precio_max_dia = data['precio_actual'] * random.uniform(1.00, 1.05)
            stock.precio_min_dia = data['precio_actual'] * random.uniform(0.95, 1.00)
            stock.volumen = random.randint(1000000, 100000000)
            stock.cambio_precio = stock.precio_actual - stock.precio_cierre_anterior
            stock.cambio_porcentaje = (stock.cambio_precio / stock.precio_cierre_anterior) * 100
            stock.ultima_actualizacion = datetime.utcnow()
            
            stocks.append(stock)
            db.session.add(stock)
        
        db.session.commit()
        print(f"✓ {len(stocks)} stocks agregados")
        
        # Devolver los IDs de los stocks creados
        stock_ids = [s.id for s in stocks]
        return stock_ids

def agregar_portfolios_ejemplo(stocks_ids):
    """Agregar portfolios de ejemplo para algunos clientes"""
    with app.app_context():
        if Portfolio.query.first():
            print("⚠ Ya existen portfolios en la base de datos")
            return
        
        print("Creando portfolios de ejemplo...")
        
        clientes = Customer.query.all()
        if not clientes:
            print("⚠ No hay clientes en la base de datos")
            return
        
        # Obtener los stocks recién creados de la base de datos
        stocks = Stock.query.filter(Stock.id.in_(stocks_ids)).all()
        
        portfolios = []
        
        # Asignar algunas acciones a los primeros 5 clientes
        for i, cliente in enumerate(clientes[:5]):
            # Cada cliente tendrá entre 2 y 5 posiciones
            num_posiciones = random.randint(2, 5)
            stocks_seleccionados = random.sample(stocks, num_posiciones)
            
            for stock in stocks_seleccionados:
                # Precio de compra ligeramente diferente al actual (simular compra anterior)
                precio_compra = float(stock.precio_actual) * random.uniform(0.80, 1.15)
                cantidad = random.choice([5, 10, 15, 20, 25, 50, 100])
                dias_atras = random.randint(30, 365)
                
                portfolio = Portfolio(
                    customer_id=cliente.id,
                    stock_id=stock.id,
                    cantidad=cantidad,
                    precio_compra=precio_compra,
                    fecha_compra=datetime.utcnow() - timedelta(days=dias_atras),
                    notas=f"Compra inicial de {stock.simbolo}"
                )
                
                portfolios.append(portfolio)
                db.session.add(portfolio)
        
        db.session.commit()
        print(f"✓ {len(portfolios)} posiciones de portfolio creadas")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Actualización BD: Stocks y Portfolio")
    print("="*60 + "\n")
    
    try:
        # 1. Actualizar tablas
        actualizar_tablas()
        
        # 2. Agregar stocks
        stock_ids = agregar_stocks_ejemplo()
        
        # 3. Agregar portfolios
        if stock_ids:
            agregar_portfolios_ejemplo(stock_ids)
        
        print("\n" + "="*60)
        print("  ✓ Base de datos actualizada con éxito!")
        print("="*60 + "\n")
        print("Ahora puedes:")
        print("  - Reiniciar la API: python app.py")
        print("  - Acceder a /api/stocks para ver las acciones")
        print("  - Acceder a /api/portfolio para ver las carteras\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
