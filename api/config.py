"""
Configuración de la aplicación.

Módulo que define las clases de configuración para diferentes entornos
de ejecución (desarrollo, producción, testing). Implementa validación
de variables de entorno críticas y configuración de componentes del sistema.

Clases:
    Config: Configuración base compartida por todos los entornos
    DevelopmentConfig: Configuración específica para desarrollo
    ProductionConfig: Configuración específica para producción
    TestConfig: Configuración específica para pruebas automatizadas
    
Uso:
    from config import config
    app.config.from_object(config['development'])
"""

import os
from typing import Dict, Type
import logging


class Config:
    """
    Configuración base de la aplicación.
    
    Define parámetros comunes a todos los entornos. Las clases derivadas
    pueden sobrescribir estos valores para entornos específicos.
    
    Attributes:
        SECRET_KEY: Clave secreta para firmar sesiones y tokens
        SQLALCHEMY_TRACK_MODIFICATIONS: Desactiva señales de modificación
        JSON_SORT_KEYS: Desactiva ordenamiento de claves en respuestas JSON
        API_KEY: Clave de autenticación para acceso a la API
        RATELIMIT_DEFAULT: Límite de peticiones por defecto
        SQLALCHEMY_ENGINE_OPTIONS: Opciones del motor de base de datos
    """
    
    # Seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_cambiar_en_produccion')
    
    # Base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
        'pool_timeout': int(os.getenv('DB_POOL_TIMEOUT', 30))
    }
    
    # API
    JSON_SORT_KEYS = False
    API_KEY = os.getenv('API_KEY', 'api_key_demo_12345')
    API_VERSION = os.getenv('API_VERSION', '1.0.0')
    
    # Rate limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'true').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS_ALLOW_HEADERS = ['Content-Type', 'X-API-Key', 'Authorization']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 10))
    
    # Stock service
    STOCK_CACHE_TIMEOUT = int(os.getenv('STOCK_CACHE_TIMEOUT', 300))  # 5 minutos
    STOCK_API_TIMEOUT = int(os.getenv('STOCK_API_TIMEOUT', 10))  # 10 segundos
    STOCK_MAX_RETRIES = int(os.getenv('STOCK_MAX_RETRIES', 3))
    
    # Paginación
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))
    
    @staticmethod
    def validate() -> None:
        """
        Valida que las variables de entorno requeridas estén presentes.
        
        Raises:
            ValueError: Si falta una variable de entorno crítica
        """
        pass  # Implementado en subclases
    
    @classmethod
    def init_app(cls, app) -> None:
        """
        Inicializa configuración adicional de la aplicación.
        
        Args:
            app: Instancia de la aplicación Flask
        """
        cls.validate()
        
        # Configurar nivel de logging
        app.logger.setLevel(getattr(logging, cls.LOG_LEVEL.upper()))


class DevelopmentConfig(Config):
    """
    Configuración para entorno de desarrollo.
    
    Activa modo debug, logging detallado y base de datos SQLite local.
    No requiere validación estricta de variables de entorno.
    """
    
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///financial.db')
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'true').lower() == 'true'
    
    # Logging más detallado en desarrollo
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
    @staticmethod
    def validate() -> None:
        """Validación mínima para desarrollo."""
        pass  # No hay validaciones críticas en desarrollo


class ProductionConfig(Config):
    """
    Configuración para entorno de producción.
    
    Desactiva modo debug, requiere variables de entorno críticas y
    aplica configuraciones de seguridad estrictas.
    """
    
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = False
    
    # Logging menos verbose en producción
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')
    
    # Rate limiting más estricto
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '50 per hour')
    
    @staticmethod
    def validate() -> None:
        """
        Validación estricta de variables de entorno para producción.
        
        Raises:
            ValueError: Si falta una variable de entorno crítica
        """
        required_vars = ['SECRET_KEY', 'DATABASE_URL', 'API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(
                f"Variables de entorno requeridas no definidas en producción: "
                f"{', '.join(missing_vars)}"
            )
        
        # Validar que SECRET_KEY no sea la por defecto
        if os.getenv('SECRET_KEY') == 'dev_secret_key_cambiar_en_produccion':
            raise ValueError(
                "SECRET_KEY debe cambiarse del valor por defecto en producción"
            )
        
        # Validar formato de DATABASE_URL
        db_url = os.getenv('DATABASE_URL', '')
        if not db_url.startswith(('postgresql://', 'mysql://', 'sqlite:///')):
            raise ValueError(
                "DATABASE_URL debe tener un formato válido "
                "(postgresql://, mysql://, o sqlite:///)"
            )


class TestConfig(Config):
    """
    Configuración para pruebas automatizadas.
    
    Utiliza base de datos en memoria y desactiva ciertas funcionalidades
    para acelerar la ejecución de tests.
    """
    
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    
    # Desactiva rate limiting en tests
    RATELIMIT_ENABLED = False
    
    # Cache desactivado en tests
    STOCK_CACHE_TIMEOUT = 0
    
    # Logging mínimo en tests
    LOG_LEVEL = 'ERROR'
    
    @staticmethod
    def validate() -> None:
        """No requiere validación en entorno de testing."""
        pass


# Diccionario de configuraciones disponibles
config: Dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Type[Config]:
    """
    Obtiene la clase de configuración para el entorno especificado.
    
    Args:
        config_name: Nombre del entorno ('development', 'production', 'testing')
                    Si es None, usa la variable de entorno FLASK_ENV o 'default'
    
    Returns:
        Type[Config]: Clase de configuración apropiada
        
    Raises:
        ValueError: Si el nombre de configuración no es válido
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    if config_name not in config:
        raise ValueError(
            f"Configuración '{config_name}' no válida. "
            f"Opciones: {', '.join(config.keys())}"
        )
    
    return config[config_name]
