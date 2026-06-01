"""
API Financiera - Aplicación principal.

Módulo principal de la aplicación Flask que proporciona servicios REST para
la gestión de transacciones financieras, clientes y análisis de portafolios.

Este módulo implementa:
- Configuración centralizada de la aplicación
- Middleware de autenticación mediante API Key
- Manejo estructurado de errores HTTP
- Sistema de logging profesional
- Validación de conexión a base de datos

Arquitectura:
    - Flask como framework web
    - SQLAlchemy como ORM
    - SQLite como base de datos
    - CORS habilitado para integraciones frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from http import HTTPStatus

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener el directorio base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))


def configure_logging(app: Flask) -> None:
    """
    Configura el sistema de logging de la aplicación.
    
    Implementa logging estructurado con rotación de archivos y diferentes
    niveles según el entorno de ejecución.
    
    Args:
        app: Instancia de la aplicación Flask
        
    Returns:
        None
    """
    # Determinar nivel de logging según entorno
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    # Crear directorio de logs si no existe
    logs_dir = os.path.join(basedir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configurar formato de log
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Handler para archivo con rotación (10MB máximo, 10 archivos de respaldo)
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'api_financiera.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configurar logger de la aplicación
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    app.logger.info('Sistema de logging configurado correctamente')


def create_app(config_name: str = None) -> Flask:
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Args:
        config_name: Nombre del entorno de configuración ('development', 'production', 'testing')
        
    Returns:
        Flask: Instancia configurada de la aplicación
    """
    app = Flask(__name__)
    
    # Configuración básica
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key and config_name == 'production':
        raise ValueError('SECRET_KEY debe estar definida en producción')
    
    app.config['SECRET_KEY'] = secret_key or 'dev_secret_key_change_in_production'
    
    # Configurar base de datos con ruta absoluta
    db_path = os.path.join(basedir, 'instance', 'financial.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # Configurar CORS con restricciones según entorno
    cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS(app, origins=cors_origins)
    
    # Configurar logging
    configure_logging(app)
    
    # Importar e inicializar base de datos
    from models import db, Customer, Transaction, AuditLog, Stock, Portfolio
    db.init_app(app)
    
    # Importar y registrar rutas
    from routes import register_routes
    register_routes(app, db)
    
    # Registrar handlers de errores
    register_error_handlers(app, db)
    
    # Registrar middleware
    register_middleware(app)
    
    return app


# Crear instancia de la aplicación
app = create_app(config_name=os.getenv('FLASK_ENV', 'development'))


def register_middleware(app: Flask) -> None:
    """
    Registra middleware de la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    @app.before_request
    def verify_api_key():
        """
        Verifica la API key en todas las peticiones excepto endpoints públicos.
        
        Returns:
            Response: Respuesta de error 401 si la autenticación falla, None si es exitosa
        """
        # Permitir peticiones OPTIONS para CORS preflight
        if request.method == 'OPTIONS':
            return None
        
        # Endpoints públicos que no requieren autenticación
        public_endpoints = ['/api/health', '/']
        
        if request.path in public_endpoints:
            return None
        
        # Verificar presencia y validez de API key
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('API_KEY', 'api_key_demo_12345')
        
        if api_key != expected_key:
            app.logger.warning(
                f'Intento de acceso no autorizado desde {request.remote_addr} '
                f'a {request.path}'
            )
            return jsonify({
                'error': 'No autorizado',
                'message': 'API key inválida o no proporcionada',
                'hint': 'Incluir header: X-API-Key'
            }), HTTPStatus.UNAUTHORIZED
    
    @app.after_request
    def log_request(response):
        """
        Registra información de cada petición procesada.
        
        Args:
            response: Respuesta HTTP generada
            
        Returns:
            Response: La misma respuesta sin modificar
        """
        app.logger.info(
            f'{request.method} {request.path} - '
            f'Status: {response.status_code} - '
            f'IP: {request.remote_addr}'
        )
        return response


def register_error_handlers(app: Flask, db) -> None:
    """
    Registra manejadores de errores HTTP.
    
    Args:
        app: Instancia de la aplicación Flask
        db: Instancia de la base de datos SQLAlchemy
    """
    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        """Maneja errores 404 - No encontrado."""
        app.logger.warning(f'Recurso no encontrado: {request.path}')
        return jsonify({
            'error': 'No encontrado',
            'message': 'El endpoint solicitado no existe',
            'path': request.path
        }), HTTPStatus.NOT_FOUND

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_error(error):
        """Maneja errores 500 - Error interno del servidor."""
        db.session.rollback()
        app.logger.error(f'Error interno del servidor: {str(error)}', exc_info=True)
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ha ocurrido un error inesperado. Por favor, contacte al administrador.'
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    
    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(error):
        """Maneja errores 400 - Petición incorrecta."""
        app.logger.warning(f'Petición incorrecta: {str(error)}')
        return jsonify({
            'error': 'Petición incorrecta',
            'message': str(error)
        }), HTTPStatus.BAD_REQUEST


# Endpoints principales
@app.route('/')
def index():
    """
    Endpoint raíz que proporciona información general de la API.
    
    Returns:
        Response: JSON con información de la API y enlaces a documentación
    """
    return jsonify({
        'message': 'API Financiera v1.0',
        'description': 'Sistema de gestión de transacciones financieras y análisis de portafolios',
        'documentation': '/api/docs',
        'endpoints': {
            'health': '/api/health',
            'customers': '/api/customers',
            'transactions': '/api/transactions',
            'portfolios': '/api/portfolios',
            'stocks': '/api/stocks',
            'reports': '/api/reports'
        },
        'version': '1.0.0'
    })


@app.route('/api/health')
def health():
    """
    Endpoint de verificación de salud del sistema.
    
    Verifica el estado de la API y la conexión a la base de datos mediante
    una consulta de prueba.
    
    Returns:
        Response: JSON con estado del sistema y componentes
    """
    try:
        # Verificar conexión a base de datos con consulta de prueba
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        app.logger.error(f'Error en health check de base de datos: {str(e)}')
        db_status = f'error: {str(e)}'
    
    health_status = {
        'status': 'ok' if db_status == 'connected' else 'degraded',
        'message': 'API Financiera v1.0',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'version': '1.0.0'
    }
    
    status_code = HTTPStatus.OK if db_status == 'connected' else HTTPStatus.SERVICE_UNAVAILABLE
    
    return jsonify(health_status), status_code


# Punto de entrada principal
if __name__ == '__main__':
    # Crear tablas de base de datos si no existen
    with app.app_context():
        from models import db
        db.create_all()
        app.logger.info('Tablas de base de datos verificadas/creadas correctamente')
    
    # Configuración del servidor
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    host = os.getenv('HOST', '0.0.0.0')
    
    # Mensaje de inicio
    app.logger.info('='*60)
    app.logger.info('API Financiera iniciada correctamente')
    app.logger.info(f'Puerto: {port}')
    app.logger.info(f'Modo debug: {debug}')
    app.logger.info(f'URL: http://localhost:{port}')
    app.logger.info('='*60)
    
    # Ejecutar servidor
    app.run(host=host, port=port, debug=debug)
