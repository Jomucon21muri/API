"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar desde la raíz del proyecto
"""

import sys
import os

# Agregar el directorio api al path para importar módulos
api_dir = os.path.join(os.path.dirname(__file__), '..', 'api')
sys.path.insert(0, api_dir)

# Cambiar al directorio api para que .env se cargue correctamente
os.chdir(api_dir)

from app import app, db
from models import Customer, Transaction
from datetime import datetime, timedelta
import random


def create_database():
    """Crear todas las tablas"""
    with app.app_context():
        print("Creando tablas...")
        db.create_all()
        print("✓ Tablas creadas exitosamente")


def populate_customers():
    """Poblar tabla de clientes"""
    with app.app_context():
        # Verificar si ya hay datos
        if Customer.query.first():
            print("⚠ Ya existen clientes en la base de datos")
            respuesta = input("¿Deseas eliminar todos los datos existentes? (s/n): ")
            if respuesta.lower() != 's':
                return
            
            # Eliminar datos existentes
            db.session.query(Transaction).delete()
            db.session.query(Customer).delete()
            db.session.commit()
            print("✓ Datos existentes eliminados")
        
        print("Creando clientes de ejemplo...")
        
        clientes_data = [
            {'email': 'maria.garcia@email.com', 'nombre': 'María', 'apellido': 'García', 'pais': 'ES', 'telefono': '+34600111222'},
            {'email': 'john.smith@email.com', 'nombre': 'John', 'apellido': 'Smith', 'pais': 'US', 'telefono': '+1555123456'},
            {'email': 'pierre.dubois@email.com', 'nombre': 'Pierre', 'apellido': 'Dubois', 'pais': 'FR', 'telefono': '+33612345678'},
            {'email': 'ana.martinez@email.com', 'nombre': 'Ana', 'apellido': 'Martínez', 'pais': 'MX', 'telefono': '+525512345678'},
            {'email': 'carlos.rodriguez@email.com', 'nombre': 'Carlos', 'apellido': 'Rodríguez', 'pais': 'ES', 'telefono': '+34600222333'},
            {'email': 'laura.fernandez@email.com', 'nombre': 'Laura', 'apellido': 'Fernández', 'pais': 'ES', 'telefono': '+34600333444'},
            {'email': 'david.lopez@email.com', 'nombre': 'David', 'apellido': 'López', 'pais': 'ES', 'telefono': '+34600444555'},
            {'email': 'elena.sanchez@email.com', 'nombre': 'Elena', 'apellido': 'Sánchez', 'pais': 'ES', 'telefono': '+34600555666'},
            {'email': 'miguel.torres@email.com', 'nombre': 'Miguel', 'apellido': 'Torres', 'pais': 'MX', 'telefono': '+525512346789'},
            {'email': 'sofia.ramirez@email.com', 'nombre': 'Sofía', 'apellido': 'Ramírez', 'pais': 'MX', 'telefono': '+525512347890'},
            {'email': 'james.wilson@email.com', 'nombre': 'James', 'apellido': 'Wilson', 'pais': 'US', 'telefono': '+1555234567'},
            {'email': 'lisa.anderson@email.com', 'nombre': 'Lisa', 'apellido': 'Anderson', 'pais': 'US', 'telefono': '+1555345678'},
            {'email': 'thomas.brown@email.com', 'nombre': 'Thomas', 'apellido': 'Brown', 'pais': 'GB', 'telefono': '+447700123456'},
            {'email': 'emma.davis@email.com', 'nombre': 'Emma', 'apellido': 'Davis', 'pais': 'GB', 'telefono': '+447700234567'},
            {'email': 'lucas.silva@email.com', 'nombre': 'Lucas', 'apellido': 'Silva', 'pais': 'BR', 'telefono': '+5511987654321'},
        ]
        
        clientes = []
        for data in clientes_data:
            cliente = Customer(**data)
            clientes.append(cliente)
            db.session.add(cliente)
        
        db.session.commit()
        print(f"✓ {len(clientes)} clientes creados")
        
        return clientes


def populate_transactions(clientes):
    """Poblar tabla de transacciones"""
    with app.app_context():
        print("Creando transacciones de ejemplo...")
        
        tipos_transaccion = ['payment', 'refund', 'transfer']
        estados = ['completed', 'pending', 'failed']
        monedas_por_pais = {
            'ES': 'EUR',
            'US': 'USD',
            'FR': 'EUR',
            'MX': 'MXN',
            'GB': 'GBP',
            'BR': 'BRL'
        }
        
        descripciones = [
            'Suscripción mensual',
            'Compra de productos',
            'Consultoría profesional',
            'Servicio premium',
            'Renovación anual',
            'Proyecto especial',
            'Pago único',
            'Mantenimiento',
            'Curso online',
            'Material adicional'
        ]
        
        transacciones = []
        
        # Crear entre 3-10 transacciones por cliente
        for cliente in clientes:
            num_transacciones = random.randint(3, 10)
            
            for _ in range(num_transacciones):
                # Fecha aleatoria en los últimos 90 días
                dias_atras = random.randint(0, 90)
                fecha = datetime.utcnow() - timedelta(days=dias_atras)
                
                # Monto aleatorio
                if random.random() < 0.1:  # 10% transacciones grandes
                    monto = round(random.uniform(1000, 5000), 2)
                else:
                    monto = round(random.uniform(10, 500), 2)
                
                # Tipo y estado
                tipo = random.choice(tipos_transaccion)
                if tipo == 'refund':
                    estado = 'completed'
                else:
                    estado = random.choices(estados, weights=[0.8, 0.15, 0.05])[0]
                
                # Moneda según país del cliente
                moneda = monedas_por_pais.get(cliente.pais, 'USD')
                
                transaccion = Transaction(
                    customer_id=cliente.id,
                    monto=monto,
                    moneda=moneda,
                    tipo=tipo,
                    estado=estado,
                    descripcion=random.choice(descripciones),
                    fecha=fecha,
                    fecha_completado=fecha if estado == 'completed' else None
                )
                
                transacciones.append(transaccion)
                db.session.add(transaccion)
        
        db.session.commit()
        print(f"✓ {len(transacciones)} transacciones creadas")


def show_statistics():
    """Mostrar estadísticas de la base de datos"""
    with app.app_context():
        num_clientes = Customer.query.count()
        num_transacciones = Transaction.query.count()
        
        total_monto = db.session.query(func.sum(Transaction.monto)).scalar() or 0
        
        print("\n" + "="*50)
        print("ESTADÍSTICAS DE LA BASE DE DATOS")
        print("="*50)
        print(f"Total de clientes: {num_clientes}")
        print(f"Total de transacciones: {num_transacciones}")
        print(f"Monto total procesado: ${total_monto:.2f}")
        print(f"Promedio por transacción: ${total_monto/num_transacciones:.2f}")
        print("="*50 + "\n")


if __name__ == '__main__':
    from sqlalchemy import func
    
    print("""
╔═══════════════════════════════════════════════╗
║  Script de Población de Base de Datos        ║
║  API Financiera                               ║
╚═══════════════════════════════════════════════╝
    """)
    
    try:
        # 1. Crear base de datos
        create_database()
        
        # 2. Crear clientes
        clientes = populate_customers()
        
        # 3. Crear transacciones
        if clientes:
            populate_transactions(clientes)
        
        # 4. Mostrar estadísticas
        show_statistics()
        
        print("✓ Base de datos poblada exitosamente!")
        print("\nPuedes iniciar la API con: python api/app.py")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
