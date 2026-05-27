"""
Script para expandir la base de datos con más clientes y portfolios
Ejecutar desde el directorio api: python expand_database.py
"""

from app import app, db
from models import Customer, Transaction, Stock, Portfolio
from datetime import datetime, timedelta
import random

def expand_customers():
    """Agregar más clientes a la base de datos"""
    with app.app_context():
        print("Expandiendo base de clientes...")
        
        existing_count = Customer.query.count()
        print(f"Clientes existentes: {existing_count}")
        
        # Nuevos clientes a agregar
        nuevos_clientes = [
            # España
            {'email': 'javier.moreno@email.com', 'nombre': 'Javier', 'apellido': 'Moreno', 'pais': 'ES', 'telefono': '+34600666777'},
            {'email': 'carmen.ruiz@email.com', 'nombre': 'Carmen', 'apellido': 'Ruiz', 'pais': 'ES', 'telefono': '+34600777888'},
            {'email': 'antonio.jimenez@email.com', 'nombre': 'Antonio', 'apellido': 'Jiménez', 'pais': 'ES', 'telefono': '+34600888999'},
            {'email': 'isabel.navarro@email.com', 'nombre': 'Isabel', 'apellido': 'Navarro', 'pais': 'ES', 'telefono': '+34600999000'},
            {'email': 'francisco.romero@email.com', 'nombre': 'Francisco', 'apellido': 'Romero', 'pais': 'ES', 'telefono': '+34600000111'},
            
            # México
            {'email': 'luis.herrera@email.com', 'nombre': 'Luis', 'apellido': 'Herrera', 'pais': 'MX', 'telefono': '+525512348901'},
            {'email': 'gabriela.castro@email.com', 'nombre': 'Gabriela', 'apellido': 'Castro', 'pais': 'MX', 'telefono': '+525512349012'},
            {'email': 'roberto.ortiz@email.com', 'nombre': 'Roberto', 'apellido': 'Ortiz', 'pais': 'MX', 'telefono': '+525512350123'},
            {'email': 'patricia.vargas@email.com', 'nombre': 'Patricia', 'apellido': 'Vargas', 'pais': 'MX', 'telefono': '+525512351234'},
            
            # Estados Unidos
            {'email': 'michael.johnson@email.com', 'nombre': 'Michael', 'apellido': 'Johnson', 'pais': 'US', 'telefono': '+1555234567'},
            {'email': 'jennifer.williams@email.com', 'nombre': 'Jennifer', 'apellido': 'Williams', 'pais': 'US', 'telefono': '+1555345678'},
            {'email': 'robert.brown@email.com', 'nombre': 'Robert', 'apellido': 'Brown', 'pais': 'US', 'telefono': '+1555456789'},
            {'email': 'sarah.davis@email.com', 'nombre': 'Sarah', 'apellido': 'Davis', 'pais': 'US', 'telefono': '+1555567890'},
            
            # Francia
            {'email': 'sophie.martin@email.com', 'nombre': 'Sophie', 'apellido': 'Martin', 'pais': 'FR', 'telefono': '+33623456789'},
            {'email': 'lucas.bernard@email.com', 'nombre': 'Lucas', 'apellido': 'Bernard', 'pais': 'FR', 'telefono': '+33634567890'},
            {'email': 'emma.petit@email.com', 'nombre': 'Emma', 'apellido': 'Petit', 'pais': 'FR', 'telefono': '+33645678901'},
            
            # Alemania
            {'email': 'hans.mueller@email.com', 'nombre': 'Hans', 'apellido': 'Müller', 'pais': 'DE', 'telefono': '+491701234567'},
            {'email': 'anna.schmidt@email.com', 'nombre': 'Anna', 'apellido': 'Schmidt', 'pais': 'DE', 'telefono': '+491702345678'},
            
            # Italia
            {'email': 'marco.rossi@email.com', 'nombre': 'Marco', 'apellido': 'Rossi', 'pais': 'IT', 'telefono': '+393331234567'},
            {'email': 'giulia.ferrari@email.com', 'nombre': 'Giulia', 'apellido': 'Ferrari', 'pais': 'IT', 'telefono': '+393332345678'},
            
            # Argentina
            {'email': 'diego.gonzalez@email.com', 'nombre': 'Diego', 'apellido': 'González', 'pais': 'AR', 'telefono': '+541112345678'},
            {'email': 'valentina.perez@email.com', 'nombre': 'Valentina', 'apellido': 'Pérez', 'pais': 'AR', 'telefono': '+541123456789'},
            
            # Colombia
            {'email': 'andres.lopez@email.com', 'nombre': 'Andrés', 'apellido': 'López', 'pais': 'CO', 'telefono': '+573001234567'},
            {'email': 'camila.rodriguez@email.com', 'nombre': 'Camila', 'apellido': 'Rodríguez', 'pais': 'CO', 'telefono': '+573002345678'},
            
            # Brasil
            {'email': 'paulo.silva@email.com', 'nombre': 'Paulo', 'apellido': 'Silva', 'pais': 'BR', 'telefono': '+5511987654321'},
            {'email': 'ana.santos@email.com', 'nombre': 'Ana', 'apellido': 'Santos', 'pais': 'BR', 'telefono': '+5511987654322'},
            
            # Reino Unido
            {'email': 'james.wilson@email.com', 'nombre': 'James', 'apellido': 'Wilson', 'pais': 'GB', 'telefono': '+447911123456'},
            {'email': 'emily.taylor@email.com', 'nombre': 'Emily', 'apellido': 'Taylor', 'pais': 'GB', 'telefono': '+447911234567'},
            
            # Canadá
            {'email': 'oliver.anderson@email.com', 'nombre': 'Oliver', 'apellido': 'Anderson', 'pais': 'CA', 'telefono': '+16131234567'},
            {'email': 'charlotte.thomas@email.com', 'nombre': 'Charlotte', 'apellido': 'Thomas', 'pais': 'CA', 'telefono': '+16132345678'},
        ]
        
        clientes_nuevos = []
        for data in nuevos_clientes:
            # Verificar si ya existe
            if not Customer.query.filter_by(email=data['email']).first():
                cliente = Customer(**data)
                clientes_nuevos.append(cliente)
                db.session.add(cliente)
        
        if clientes_nuevos:
            db.session.commit()
            print(f"✓ {len(clientes_nuevos)} nuevos clientes agregados")
        else:
            print("⚠ Todos los clientes ya existen")
        
        total = Customer.query.count()
        print(f"Total de clientes en BD: {total}")
        return total

def create_transactions_for_all():
    """Crear transacciones para todos los clientes"""
    with app.app_context():
        print("\nCreando transacciones para todos los clientes...")
        
        clientes = Customer.query.all()
        monedas = {
            'ES': 'EUR', 'US': 'USD', 'FR': 'EUR', 'MX': 'MXN', 
            'DE': 'EUR', 'IT': 'EUR', 'AR': 'ARS', 'CO': 'COP',
            'BR': 'BRL', 'GB': 'GBP', 'CA': 'CAD'
        }
        
        tipos = ['payment', 'refund', 'transfer', 'subscription', 'purchase']
        estados = ['completed', 'pending', 'processing']
        descripciones = [
            'Suscripción mensual premium',
            'Compra de productos',
            'Consultoría financiera',
            'Servicio de gestión de cartera',
            'Comisión por trading',
            'Renovación anual',
            'Pago de dividendos',
            'Transferencia internacional',
            'Depósito inicial',
            'Retiro de fondos'
        ]
        
        transacciones_nuevas = 0
        for cliente in clientes:
            # Clientes sin transacciones o con pocas, agregar más
            trans_existentes = Transaction.query.filter_by(customer_id=cliente.id).count()
            
            if trans_existentes < 5:
                num_trans = random.randint(5, 15)
                for _ in range(num_trans):
                    dias_atras = random.randint(0, 365)
                    fecha = datetime.utcnow() - timedelta(days=dias_atras)
                    monto = round(random.uniform(10, 2000), 2)
                    
                    trans = Transaction(
                        customer_id=cliente.id,
                        monto=monto,
                        moneda=monedas.get(cliente.pais, 'USD'),
                        tipo=random.choice(tipos),
                        estado=random.choice(estados),
                        descripcion=random.choice(descripciones),
                        fecha=fecha
                    )
                    db.session.add(trans)
                    transacciones_nuevas += 1
        
        if transacciones_nuevas > 0:
            db.session.commit()
            print(f"✓ {transacciones_nuevas} transacciones creadas")
        
        total = Transaction.query.count()
        print(f"Total de transacciones en BD: {total}")

def create_portfolios_for_all():
    """Crear portfolios para todos los clientes que no tengan"""
    with app.app_context():
        print("\nCreando portfolios para todos los clientes...")
        
        # Obtener todos los clientes y stocks
        clientes = Customer.query.all()
        stocks = Stock.query.all()
        
        if not stocks:
            print("⚠ No hay stocks en la BD. Ejecuta update_db_stocks.py primero")
            return
        
        portfolios_creados = 0
        
        for cliente in clientes:
            # Verificar si ya tiene portfolio
            portfolio_existente = Portfolio.query.filter_by(
                customer_id=cliente.id, 
                activo=True
            ).first()
            
            if portfolio_existente:
                continue  # Ya tiene portfolio
            
            # Crear portfolio con 2-6 posiciones aleatorias
            num_posiciones = random.randint(2, 6)
            stocks_seleccionados = random.sample(stocks, min(num_posiciones, len(stocks)))
            
            for stock in stocks_seleccionados:
                # Simular compra en el pasado
                dias_atras = random.randint(30, 730)  # Entre 1 mes y 2 años
                fecha_compra = datetime.utcnow() - timedelta(days=dias_atras)
                
                # Cantidad aleatoria
                cantidad = random.choice([5, 10, 15, 20, 25, 50, 75, 100])
                
                # Precio de compra simulado (puede ser más bajo o más alto que el actual)
                variacion = random.uniform(0.70, 1.30)  # ±30%
                precio_compra = float(stock.precio_actual) * variacion
                
                portfolio = Portfolio(
                    customer_id=cliente.id,
                    stock_id=stock.id,
                    cantidad=cantidad,
                    precio_compra=round(precio_compra, 2),
                    fecha_compra=fecha_compra,
                    notas=f"Compra automática de {stock.simbolo}"
                )
                
                db.session.add(portfolio)
                portfolios_creados += 1
        
        if portfolios_creados > 0:
            db.session.commit()
            print(f"✓ {portfolios_creados} posiciones de portfolio creadas")
        else:
            print("⚠ Todos los clientes ya tienen portfolios")
        
        # Estadísticas
        total_portfolios = Portfolio.query.filter_by(activo=True).count()
        clientes_con_portfolio = db.session.query(Portfolio.customer_id).filter_by(activo=True).distinct().count()
        print(f"Total de posiciones activas: {total_portfolios}")
        print(f"Clientes con portfolio: {clientes_con_portfolio}/{len(clientes)}")

def show_statistics():
    """Mostrar estadísticas de la base de datos"""
    with app.app_context():
        print("\n" + "="*60)
        print("  ESTADÍSTICAS DE LA BASE DE DATOS")
        print("="*60)
        
        total_customers = Customer.query.count()
        active_customers = Customer.query.filter_by(activo=True).count()
        
        total_transactions = Transaction.query.count()
        completed_trans = Transaction.query.filter_by(estado='completed').count()
        
        total_stocks = Stock.query.count()
        
        total_portfolios = Portfolio.query.filter_by(activo=True).count()
        customers_with_portfolio = db.session.query(Portfolio.customer_id).filter_by(activo=True).distinct().count()
        
        # Agrupar clientes por país
        from sqlalchemy import func
        paises = db.session.query(
            Customer.pais, 
            func.count(Customer.id)
        ).group_by(Customer.pais).all()
        
        print(f"\nClientes:")
        print(f"  - Total: {total_customers}")
        print(f"  - Activos: {active_customers}")
        print(f"\n  Por país:")
        for pais, count in sorted(paises, key=lambda x: x[1], reverse=True):
            print(f"    - {pais}: {count}")
        
        print(f"\nTransacciones:")
        print(f"  - Total: {total_transactions}")
        print(f"  - Completadas: {completed_trans}")
        print(f"  - Promedio por cliente: {total_transactions/total_customers:.1f}")
        
        print(f"\nAcciones:")
        print(f"  - Total disponibles: {total_stocks}")
        
        print(f"\nPortfolios:")
        print(f"  - Posiciones activas: {total_portfolios}")
        print(f"  - Clientes con portfolio: {customers_with_portfolio}")
        print(f"  - Promedio posiciones/cliente: {total_portfolios/max(customers_with_portfolio, 1):.1f}")
        
        print("\n" + "="*60)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  EXPANSIÓN DE BASE DE DATOS")
    print("="*60 + "\n")
    
    try:
        # 1. Expandir clientes
        total_clientes = expand_customers()
        
        # 2. Crear transacciones para todos
        create_transactions_for_all()
        
        # 3. Crear portfolios para todos
        create_portfolios_for_all()
        
        # 4. Mostrar estadísticas
        show_statistics()
        
        print("\n" + "="*60)
        print("  ✓ Base de datos expandida exitosamente!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
