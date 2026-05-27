"""
Script de inicialización simple para crear base de datos
Ejecutar desde el directorio api: python init_db.py
"""

from app import app, db
from models import Customer, Transaction, AuditLog
from datetime import datetime, timedelta
import random

def create_database():
    """Crear todas las tablas"""
    with app.app_context():
        print("Creando tablas...")
        db.create_all()
        print("✓ Tablas creadas exitosamente")

def add_sample_data():
    """Agregar datos de ejemplo"""
    with app.app_context():
        # Verificar si ya hay datos
        if Customer.query.first():
            print("⚠ Ya existen datos en la base de datos")
            return
        
        print("Creando clientes de ejemplo...")
        
        # Crear clientes
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
        ]
        
        clientes = []
        for data in clientes_data:
            cliente = Customer(**data)
            clientes.append(cliente)
            db.session.add(cliente)
        
        db.session.commit()
        print(f"✓ {len(clientes)} clientes creados")
        
        # Crear transacciones
        print("Creando transacciones de ejemplo...")
        
        tipos = ['payment', 'refund', 'transfer']
        estados = ['completed', 'pending']
        monedas = {'ES': 'EUR', 'US': 'USD', 'FR': 'EUR', 'MX': 'MXN'}
        descripciones = ['Suscripción mensual', 'Compra de productos', 'Consultoría', 'Servicio premium']
        
        transacciones = []
        for cliente in clientes:
            num_trans = random.randint(3, 7)
            for _ in range(num_trans):
                dias_atras = random.randint(0, 90)
                fecha = datetime.utcnow() - timedelta(days=dias_atras)
                monto = round(random.uniform(10, 500), 2)
                
                trans = Transaction(
                    customer_id=cliente.id,
                    monto=monto,
                    moneda=monedas.get(cliente.pais, 'USD'),
                    tipo=random.choice(tipos),
                    estado=random.choice(estados),
                    descripcion=random.choice(descripciones),
                    fecha=fecha
                )
                transacciones.append(trans)
                db.session.add(trans)
        
        db.session.commit()
        print(f"✓ {len(transacciones)} transacciones creadas")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Inicialización de Base de Datos")
    print("="*50 + "\n")
    
    try:
        create_database()
        add_sample_data()
        
        print("\n" + "="*50)
        print("  ✓ Base de datos lista!")
        print("="*50 + "\n")
        print("Puedes iniciar la API con: python app.py\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
