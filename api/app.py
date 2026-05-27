"""
API Financiera - Aplicación principal
Servidor Flask con endpoints REST para gestión de transacciones y clientes
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener el directorio base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')

# Configurar base de datos con ruta absoluta
db_path = os.path.join(basedir, 'instance', 'financial.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Habilitar CORS
CORS(app)

# Importar e inicializar base de datos
from models import db, Customer, Transaction, AuditLog, Stock, Portfolio

# Inicializar db con la aplicación Flask
db.init_app(app)

# Importar rutas
from routes import register_routes

# Registrar todas las rutas
register_routes(app, db)


# Middleware de autenticación
@app.before_request
def verify_api_key():
    """Verificar API key en todas las peticiones excepto /health"""
    # Permitir peticiones OPTIONS (CORS preflight)
    if request.method == 'OPTIONS':
        return None
    
    # Endpoints públicos (sin autenticación)
    public_endpoints = ['/api/health', '/']
    
    if request.path in public_endpoints:
        return None
    
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    expected_key = os.getenv('API_KEY', 'api_key_demo_12345')
    
    if api_key != expected_key:
        return jsonify({
            'error': 'No autorizado',
            'message': 'API key inválida o no proporcionada',
            'hint': 'Incluir header: X-API-Key'
        }), 401


# Manejador de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'No encontrado',
        'message': 'El endpoint solicitado no existe',
        'path': request.path
    }), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'error': 'Error interno del servidor',
        'message': str(error)
    }), 500


# Endpoint raíz
@app.route('/')
def index():
    return jsonify({
        'message': 'API Financiera v1.0',
        'documentation': '/api/docs',
        'endpoints': {
            'health': '/api/health',
            'customers': '/api/customers',
            'transactions': '/api/transactions',
            'reports': '/api/reports'
        }
    })


# Endpoint de salud
@app.route('/api/health')
def health():
    """Verificar estado de la API y conexión a base de datos"""
    try:
        # Verificar conexión a base de datos
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'ok',
        'message': 'API Financiera v1.0',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'version': '1.0.0'
    })


# Iniciar servidor
if __name__ == '__main__':
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    # Ejecutar servidor
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"""
    ╔═══════════════════════════════════════╗
    ║   API Financiera Iniciada             ║
    ║   Puerto: {port}                          ║
    ║   Debug: {debug}                         ║
    ║   URL: http://localhost:{port}        ║
    ╚═══════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
