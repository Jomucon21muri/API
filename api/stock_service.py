"""
Servicio de integración con mercado de valores.

Este módulo proporciona funcionalidades para consultar datos de acciones
en tiempo real utilizando la librería yfinance (Yahoo Finance API).

Características:
- Actualización de precios en tiempo real
- Caché de resultados para optimización
- Manejo robusto de errores con reintentos
- Soporte para consultas masivas (batch)
- Datos históricos de precios

Dependencias:
    - yfinance: Cliente para Yahoo Finance API
    - functools: Para decoradores de caché
    
Uso:
    from stock_service import StockService
    
    # Actualizar precio de una acción
    stock = StockService.actualizar_precio('AAPL')
    
    # Obtener datos históricos
    history = StockService.obtener_historico('MSFT', periodo='1mo')
"""

import yfinance as yf
from datetime import datetime, timedelta
from models import Stock, db
from functools import lru_cache
from typing import Optional, List, Dict, Any
import logging
import time

# Configurar logger
logger = logging.getLogger(__name__)


class StockServiceError(Exception):
    """Excepción base para errores del servicio de acciones."""
    pass


class StockNotFoundError(StockServiceError):
    """Excepción lanzada cuando no se encuentra una acción."""
    pass


class StockAPIError(StockServiceError):
    """Excepción lanzada cuando la API externa falla."""
    pass


class StockService:
    """
    Servicio para gestión de datos del mercado de valores.
    
    Proporciona métodos para consultar y actualizar información de acciones
    utilizando Yahoo Finance como fuente de datos. Implementa caché local
    y manejo de errores robusto.
    
    Attributes:
        CACHE_TIMEOUT: Tiempo en segundos para validez del caché (300s = 5min)
        MAX_RETRIES: Número máximo de reintentos en caso de fallo
        RETRY_DELAY: Segundos de espera entre reintentos
    """
    
    CACHE_TIMEOUT = 300  # 5 minutos
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # segundos
    API_TIMEOUT = 10  # segundos
    
    @staticmethod
    def _retry_on_failure(func):
        """
        Decorador para reintentar operaciones que fallan.
        
        Args:
            func: Función a decorar
            
        Returns:
            Función decorada con lógica de reintentos
        """
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(StockService.MAX_RETRIES):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < StockService.MAX_RETRIES - 1:
                        logger.warning(
                            f'Intento {attempt + 1} fallido para {func.__name__}: {str(e)}. '
                            f'Reintentando en {StockService.RETRY_DELAY}s...'
                        )
                        time.sleep(StockService.RETRY_DELAY)
                    else:
                        logger.error(
                            f'Todos los intentos fallaron para {func.__name__}: {str(e)}'
                        )
            
            raise StockAPIError(
                f'Operación {func.__name__} falló después de {StockService.MAX_RETRIES} intentos'
            ) from last_exception
        
        return wrapper
    
    @staticmethod
    @_retry_on_failure
    def actualizar_precio(simbolo: str) -> Optional[Stock]:
        """
        Actualiza el precio de una acción específica en la base de datos.
        
        Obtiene los datos más recientes de Yahoo Finance y actualiza o crea
        el registro correspondiente en la base de datos. Incluye precio actual,
        apertura, máximo, mínimo, volumen y cambios porcentuales.
        
        Args:
            simbolo: Símbolo de la acción (ej: 'AAPL', 'MSFT')
            
        Returns:
            Stock: Objeto Stock actualizado, o None si no se encuentra
            
        Raises:
            StockNotFoundError: Si la acción no existe
            StockAPIError: Si hay un error comunicándose con la API
            
        Example:
            >>> stock = StockService.actualizar_precio('AAPL')
            >>> print(f'{stock.simbolo}: ${stock.precio_actual}')
            AAPL: $150.25
        """
        try:
            simbolo = simbolo.upper().strip()
            logger.info(f'Actualizando precio para {simbolo}')
            
            ticker = yf.Ticker(simbolo)
            info = ticker.info
            hist = ticker.history(period='1d')
            
            if hist.empty:
                logger.warning(f'No se encontraron datos para {simbolo}')
                raise StockNotFoundError(f'No hay datos disponibles para {simbolo}')
            
            # Obtener última fila de datos
            last_row = hist.iloc[-1]
            
            # Buscar o crear stock en base de datos
            stock = Stock.query.filter_by(simbolo=simbolo).first()
            
            if not stock:
                logger.info(f'Creando nuevo registro para {simbolo}')
                stock = Stock(
                    simbolo=simbolo,
                    nombre=info.get('longName', simbolo),
                    sector=info.get('sector'),
                    mercado=info.get('exchange'),
                    moneda=info.get('currency', 'USD')
                )
                db.session.add(stock)
            
            # Actualizar precios
            stock.precio_actual = float(last_row['Close'])
            stock.precio_apertura = float(last_row['Open'])
            stock.precio_max_dia = float(last_row['High'])
            stock.precio_min_dia = float(last_row['Low'])
            stock.volumen = int(last_row['Volume'])
            
            # Calcular cambios respecto al cierre anterior
            if info.get('previousClose'):
                stock.precio_cierre_anterior = float(info['previousClose'])
                stock.cambio_precio = stock.precio_actual - stock.precio_cierre_anterior
                stock.cambio_porcentaje = (
                    (stock.cambio_precio / stock.precio_cierre_anterior) * 100
                )
            
            stock.ultima_actualizacion = datetime.utcnow()
            
            db.session.commit()
            logger.info(f'Precio actualizado para {simbolo}: ${stock.precio_actual}')
            
            return stock
        
        except StockNotFoundError:
            raise
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error actualizando precio de {simbolo}: {str(e)}')
            raise StockAPIError(f'Error al obtener datos de {simbolo}') from e
    
    @staticmethod
    @_retry_on_failure
    def obtener_multiples_precios(simbolos: List[str]) -> List[Dict[str, Any]]:
        """
        Obtiene precios de múltiples acciones en una sola operación.
        
        Optimiza las consultas a la API utilizando batch requests. Cada acción
        que falle se omite y se continúa con las demás.
        
        Args:
            simbolos: Lista de símbolos de acciones
            
        Returns:
            List[Dict]: Lista de diccionarios con datos de cada acción
            
        Example:
            >>> precios = StockService.obtener_multiples_precios(['AAPL', 'MSFT', 'GOOGL'])
            >>> for accion in precios:
            ...     print(f"{accion['simbolo']}: ${accion['precio_actual']}")
        """
        if not simbolos:
            return []
        
        simbolos = [s.upper().strip() for s in simbolos]
        logger.info(f'Obteniendo precios para {len(simbolos)} acciones')
        
        try:
            tickers = yf.Tickers(' '.join(simbolos))
            resultados = []
            
            for simbolo in simbolos:
                try:
                    ticker = tickers.tickers[simbolo]
                    hist = ticker.history(period='1d')
                    
                    if not hist.empty:
                        last_row = hist.iloc[-1]
                        info = ticker.info
                        
                        resultados.append({
                            'simbolo': simbolo,
                            'nombre': info.get('longName', simbolo),
                            'precio_actual': float(last_row['Close']),
                            'precio_apertura': float(last_row['Open']),
                            'precio_max_dia': float(last_row['High']),
                            'precio_min_dia': float(last_row['Low']),
                            'volumen': int(last_row['Volume']),
                            'cambio_porcentaje': float(info.get('regularMarketChangePercent', 0)),
                            'moneda': info.get('currency', 'USD'),
                            'sector': info.get('sector'),
                            'mercado': info.get('exchange')
                        })
                        logger.debug(f'Datos obtenidos para {simbolo}')
                    else:
                        logger.warning(f'No hay datos disponibles para {simbolo}')
                        
                except Exception as e:
                    logger.warning(f'Error procesando {simbolo}: {str(e)}')
                    continue
            
            logger.info(f'Se obtuvieron datos de {len(resultados)}/{len(simbolos)} acciones')
            return resultados
        
        except Exception as e:
            logger.error(f'Error obteniendo múltiples precios: {str(e)}')
            raise StockAPIError('Error en consulta masiva de precios') from e
    
    @staticmethod
    @lru_cache(maxsize=128)
    def obtener_historico(
        simbolo: str, 
        periodo: str = '1mo',
        intervalo: str = '1d'
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Obtiene datos históricos de precios de una acción.
        
        Los resultados se almacenan en caché para mejorar rendimiento en
        consultas repetidas.
        
        Args:
            simbolo: Símbolo de la acción
            periodo: Período de tiempo ('1d', '5d', '1mo', '3mo', '6mo', '1y', 
                    '2y', '5y', '10y', 'ytd', 'max')
            intervalo: Intervalo de los datos ('1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo')
            
        Returns:
            List[Dict]: Lista de diccionarios con datos históricos, o None si falla
            
        Example:
            >>> historico = StockService.obtener_historico('AAPL', periodo='3mo')
            >>> print(f'Registros históricos: {len(historico)}')
            Registros históricos: 63
        """
        try:
            simbolo = simbolo.upper().strip()
            logger.info(f'Obteniendo histórico de {simbolo} - Período: {periodo}')
            
            ticker = yf.Ticker(simbolo)
            hist = ticker.history(period=periodo, interval=intervalo)
            
            if hist.empty:
                logger.warning(f'No hay datos históricos para {simbolo}')
                return None
            
            # Convertir a formato JSON serializable
            datos = []
            for index, row in hist.iterrows():
                datos.append({
                    'fecha': index.strftime('%Y-%m-%d %H:%M:%S'),
                    'apertura': float(row['Open']),
                    'maximo': float(row['High']),
                    'minimo': float(row['Low']),
                    'cierre': float(row['Close']),
                    'volumen': int(row['Volume'])
                })
            
            logger.info(f'Se obtuvieron {len(datos)} registros históricos para {simbolo}')
            return datos
        
        except Exception as e:
            logger.error(f'Error obteniendo histórico de {simbolo}: {str(e)}')
            return None
    
    @staticmethod
    def buscar_accion(query: str) -> List[Dict[str, Any]]:
        """
        Busca acciones por nombre o símbolo.
        
        Nota: yfinance no proporciona una API de búsqueda robusta. Esta
        implementación intenta obtener datos del símbolo proporcionado.
        Para búsquedas más sofisticadas, considerar APIs especializadas.
        
        Args:
            query: Término de búsqueda (símbolo o nombre parcial)
            
        Returns:
            List[Dict]: Lista de acciones encontradas
        """
        try:
            query = query.upper().strip()
            logger.info(f'Buscando acción: {query}')
            
            ticker = yf.Ticker(query)
            info = ticker.info
            
            # Verificar que se obtuvieron datos válidos
            if info.get('symbol') or info.get('longName'):
                resultado = [{
                    'simbolo': info.get('symbol', query),
                    'nombre': info.get('longName', query),
                    'sector': info.get('sector'),
                    'industria': info.get('industry'),
                    'mercado': info.get('exchange'),
                    'moneda': info.get('currency', 'USD'),
                    'descripcion': info.get('longBusinessSummary', '')[:200]  # Primeros 200 caracteres
                }]
                logger.info(f'Acción encontrada: {resultado[0]["nombre"]}')
                return resultado
            
            logger.warning(f'No se encontró información para {query}')
            return []
        
        except Exception as e:
            logger.warning(f'Error buscando {query}: {str(e)}')
            return []
    
    @staticmethod
    def obtener_acciones_populares() -> List[Dict[str, Any]]:
        """
        Obtiene lista de acciones más populares del mercado.
        
        Returns:
            List[Dict]: Lista con datos de las acciones más negociadas
        """
        simbolos_populares = [
            'AAPL',  # Apple
            'MSFT',  # Microsoft
            'GOOGL', # Alphabet (Google)
            'AMZN',  # Amazon
            'TSLA',  # Tesla
            'META',  # Meta Platforms (Facebook)
            'NVDA',  # NVIDIA
            'JPM',   # JPMorgan Chase
            'V',     # Visa
            'WMT',   # Walmart
            'NFLX',  # Netflix
            'DIS',   # Disney
            'PYPL',  # PayPal
            'INTC',  # Intel
            'AMD'    # Advanced Micro Devices
        ]
        
        logger.info('Obteniendo datos de acciones populares')
        return StockService.obtener_multiples_precios(simbolos_populares)
    
    @staticmethod
    def limpiar_cache() -> None:
        """
        Limpia el caché de consultas históricas.
        
        Útil cuando se necesita forzar la actualización de datos.
        """
        StockService.obtener_historico.cache_clear()
        logger.info('Caché de datos históricos limpiado')
