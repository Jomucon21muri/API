"""
Script de inicialización y población de base de datos.

Este módulo proporciona funcionalidad para crear la estructura de base de datos
y poblarla con datos de ejemplo para propósitos de desarrollo y testing.

Uso:
    python scripts/populate_db.py

Funciones:
    create_database: Crea todas las tablas
    populate_customers: Inserta clientes de ejemplo
    populate_transactions: Inserta transacciones de ejemplo
    show_statistics: Muestra estadísticas de la BD
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import random
import logging
from typing import List, Optional

# Configurar path para importar módulos de la API
project_root = Path(__file__).parent.parent
api_dir = project_root / 'api'
sys.path.insert(0, str(api_dir))

# Cambiar al directorio API para cargar .env correctamente
os.chdir(api_dir)

from app import app, db
from models import Customer, Transaction
from sqlalchemy import func

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('populate_db.log')
    ]
)
logger = logging.getLogger(__name__)


# Datos de ejemplo para clientes
SAMPLE_CUSTOMERS = [
    {'email': 'maria.garcia@email.com', 'nombre': 'María', 'apellido': 'García', 
     'pais': 'ES', 'telefono': '+34600111222'},
    {'email': 'john.smith@email.com', 'nombre': 'John', 'apellido': 'Smith', 
     'pais': 'US', 'telefono': '+1555123456'},
    {'email': 'pierre.dubois@email.com', 'nombre': 'Pierre', 'apellido': 'Dubois', 
     'pais': 'FR', 'telefono': '+33612345678'},
    {'email': 'ana.martinez@email.com', 'nombre': 'Ana', 'apellido': 'Martínez', 
     'pais': 'MX', 'telefono': '+525512345678'},
    {'email': 'carlos.rodriguez@email.com', 'nombre': 'Carlos', 'apellido': 'Rodríguez', 
     'pais': 'ES', 'telefono': '+34600222333'},
    {'email': 'laura.fernandez@email.com', 'nombre': 'Laura', 'apellido': 'Fernández', 
     'pais': 'ES', 'telefono': '+34600333444'},
    {'email': 'david.lopez@email.com', 'nombre': 'David', 'apellido': 'López', 
     'pais': 'ES', 'telefono': '+34600444555'},
    {'email': 'elena.sanchez@email.com', 'nombre': 'Elena', 'apellido': 'Sánchez', 
     'pais': 'ES', 'telefono': '+34600555666'},
    {'email': 'miguel.torres@email.com', 'nombre': 'Miguel', 'apellido': 'Torres', 
     'pais': 'MX', 'telefono': '+525512346789'},
    {'email': 'sofia.ramirez@email.com', 'nombre': 'Sofía', 'apellido': 'Ramírez', 
     'pais': 'MX', 'telefono': '+525512347890'},
    {'email': 'james.wilson@email.com', 'nombre': 'James', 'apellido': 'Wilson', 
     'pais': 'US', 'telefono': '+1555234567'},
    {'email': 'lisa.anderson@email.com', 'nombre': 'Lisa', 'apellido': 'Anderson', 
     'pais': 'US', 'telefono': '+1555345678'},
    {'email': 'thomas.brown@email.com', 'nombre': 'Thomas', 'apellido': 'Brown', 
     'pais': 'GB', 'telefono': '+447700123456'},
    {'email': 'emma.davis@email.com', 'nombre': 'Emma', 'apellido': 'Davis', 
     'pais': 'GB', 'telefono': '+447700234567'},
    {'email': 'lucas.silva@email.com', 'nombre': 'Lucas', 'apellido': 'Silva', 
     'pais': 'BR', 'telefono': '+5511987654321'},
]

# Constantes para transacciones
TRANSACTION_TYPES = ['payment', 'refund', 'transfer']
TRANSACTION_STATES = ['completed', 'pending', 'failed']
CURRENCY_BY_COUNTRY = {
    'ES': 'EUR', 'US': 'USD', 'FR': 'EUR',
    'MX': 'MXN', 'GB': 'GBP', 'BR': 'BRL'
}
TRANSACTION_DESCRIPTIONS = [
    'Suscripción mensual', 'Compra de productos', 'Consultoría profesional',
    'Servicio premium', 'Renovación anual', 'Proyecto especial',
    'Pago único', 'Mantenimiento', 'Curso online', 'Material adicional'
]


def create_database() -> None:
    """
    Crea todas las tablas en la base de datos.
    
    Utiliza SQLAlchemy para crear las tablas definidas en models.py.
    """
    with app.app_context():
        logger.info('Iniciando creación de tablas...')
        db.create_all()
        logger.info('Tablas creadas exitosamente')


def clear_existing_data() -> None:
    """
    Elimina todos los datos existentes en la base de datos.
    
    Mantiene la estructura de tablas pero elimina todos los registros.
    """
    with app.app_context():
        logger.warning('Eliminando datos existentes...')
        db.session.query(Transaction).delete()
        db.session.query(Customer).delete()
        db.session.commit()
        logger.info('Datos existentes eliminados')


def populate_customers(clear_existing: bool = False) -> List[Customer]:
    """
    Pobla la tabla de clientes con datos de ejemplo.
    
    Args:
        clear_existing: Si True, elimina datos existentes antes de insertar
        
    Returns:
        List[Customer]: Lista de clientes creados
        
    Raises:
        RuntimeError: Si hay un error al insertar los datos
    """
    with app.app_context():
        # Verificar si ya existen datos
        existing_count = Customer.query.count()
        if existing_count > 0:
            if not clear_existing:
                logger.warning(f'Ya existen {existing_count} clientes en la BD')
                logger.info('Use clear_existing=True para eliminar datos')
                return []
            clear_existing_data()
        
        logger.info(f'Creando {len(SAMPLE_CUSTOMERS)} clientes de ejemplo...')
        
        customers = []
        for data in SAMPLE_CUSTOMERS:
            customer = Customer(**data)
            customers.append(customer)
            db.session.add(customer)
        
        try:
            db.session.commit()
            logger.info(f'{len(customers)} clientes creados exitosamente')
            return customers
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error al crear clientes: {e}')
            raise RuntimeError(f'Error al poblar clientes: {e}')


def generate_transaction_amount() -> float:
    """
    Genera un monto aleatorio para una transacción.
    
    El 10% de las transacciones son grandes (1000-5000),
    el resto son pequeñas (10-500).
    
    Returns:
        float: Monto generado con 2 decimales
    """
    if random.random() < 0.1:  # 10% transacciones grandes
        return round(random.uniform(1000, 5000), 2)
    return round(random.uniform(10, 500), 2)


def generate_transaction_date() -> datetime:
    """
    Genera una fecha aleatoria en los últimos 90 días.
    
    Returns:
        datetime: Fecha generada
    """
    days_ago = random.randint(0, 90)
    return datetime.utcnow() - timedelta(days=days_ago)


def populate_transactions(customers: List[Customer]) -> None:
    """
    Pobla la tabla de transacciones con datos de ejemplo.
    
    Crea entre 3 y 10 transacciones por cada cliente, con montos,
    estados y fechas aleatorios pero realistas.
    
    Args:
        customers: Lista de clientes para los cuales crear transacciones
        
    Raises:
        RuntimeError: Si hay un error al insertar los datos
    """
    with app.app_context():
        logger.info('Creando transacciones de ejemplo...')
        
        transactions = []
        
        for customer in customers:
            num_transactions = random.randint(3, 10)
            
            for _ in range(num_transactions):
                transaction_date = generate_transaction_date()
                amount = generate_transaction_amount()
                transaction_type = random.choice(TRANSACTION_TYPES)
                
                # Refunds siempre completados, otros con pesos diferentes
                if transaction_type == 'refund':
                    state = 'completed'
                else:
                    state = random.choices(
                        TRANSACTION_STATES, 
                        weights=[0.8, 0.15, 0.05]  # 80% completadas
                    )[0]
                
                currency = CURRENCY_BY_COUNTRY.get(customer.pais, 'USD')
                
                transaction = Transaction(
                    customer_id=customer.id,
                    monto=amount,
                    moneda=currency,
                    tipo=transaction_type,
                    estado=state,
                    descripcion=random.choice(TRANSACTION_DESCRIPTIONS),
                    fecha=transaction_date,
                    fecha_completado=transaction_date if state == 'completed' else None
                )
                
                transactions.append(transaction)
                db.session.add(transaction)
        
        try:
            db.session.commit()
            logger.info(f'{len(transactions)} transacciones creadas exitosamente')
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error al crear transacciones: {e}')
            raise RuntimeError(f'Error al poblar transacciones: {e}')


def show_statistics() -> None:
    """
    Muestra estadísticas de la base de datos poblada.
    
    Incluye conteos de registros, montos totales y promedios.
    """
    with app.app_context():
        num_customers = Customer.query.count()
        num_transactions = Transaction.query.count()
        
        total_amount = db.session.query(func.sum(Transaction.monto)).scalar() or 0
        avg_amount = total_amount / num_transactions if num_transactions > 0 else 0
        
        print('\n' + '=' * 60)
        print('ESTADÍSTICAS DE LA BASE DE DATOS')
        print('=' * 60)
        print(f'Total de clientes:        {num_customers}')
        print(f'Total de transacciones:   {num_transactions}')
        print(f'Monto total procesado:    ${total_amount:.2f}')
        print(f'Promedio por transacción: ${avg_amount:.2f}')
        print('=' * 60 + '\n')
        
        logger.info(f'BD poblada: {num_customers} clientes, {num_transactions} transacciones')


def main() -> None:
    """
    Función principal del script de población.
    
    Coordina la creación de estructura y población de datos.
    """
    print("""
╔════════════════════════════════════════════════════════════╗
║  Script de Inicialización de Base de Datos                ║
║  Sistema de Gestión Financiera                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Paso 1: Crear estructura de BD
        create_database()
        
        # Paso 2: Poblar clientes (con confirmación si ya existen)
        customers = populate_customers(clear_existing=True)
        
        # Paso 3: Poblar transacciones
        if customers:
            populate_transactions(customers)
        
        # Paso 4: Mostrar estadísticas
        show_statistics()
        
        print('Base de datos inicializada exitosamente')
        print('\nInicie la API con: python api/app.py')
        
    except Exception as e:
        logger.error(f'Error durante la población: {e}', exc_info=True)
        print(f'\nError: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
