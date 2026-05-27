"""
Servicio para obtener datos de acciones en tiempo real
Utiliza yfinance para conectarse a Yahoo Finance
"""

import yfinance as yf
from datetime import datetime
from models import Stock, db


class StockService:
    """Servicio para gestionar datos de acciones"""
    
    @staticmethod
    def actualizar_precio(simbolo):
        """Actualizar precio de una acción específica"""
        try:
            ticker = yf.Ticker(simbolo)
            info = ticker.info
            hist = ticker.history(period='1d')
            
            if hist.empty:
                return None
            
            # Obtener última fila
            last_row = hist.iloc[-1]
            
            # Buscar o crear stock
            stock = Stock.query.filter_by(simbolo=simbolo.upper()).first()
            
            if not stock:
                stock = Stock(
                    simbolo=simbolo.upper(),
                    nombre=info.get('longName', simbolo),
                    sector=info.get('sector'),
                    mercado=info.get('exchange'),
                    moneda=info.get('currency', 'USD')
                )
                db.session.add(stock)
            
            # Actualizar precios
            stock.precio_actual = last_row['Close']
            stock.precio_apertura = last_row['Open']
            stock.precio_max_dia = last_row['High']
            stock.precio_min_dia = last_row['Low']
            stock.volumen = last_row['Volume']
            
            # Calcular cambios
            if info.get('previousClose'):
                stock.precio_cierre_anterior = info['previousClose']
                stock.cambio_precio = stock.precio_actual - stock.precio_cierre_anterior
                stock.cambio_porcentaje = (stock.cambio_precio / stock.precio_cierre_anterior) * 100
            
            stock.ultima_actualizacion = datetime.utcnow()
            
            db.session.commit()
            
            return stock
        
        except Exception as e:
            print(f"Error actualizando {simbolo}: {e}")
            return None
    
    @staticmethod
    def obtener_multiples_precios(simbolos):
        """Obtener precios de múltiples acciones"""
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
                            'simbolo': simbolo.upper(),
                            'nombre': info.get('longName', simbolo),
                            'precio_actual': float(last_row['Close']),
                            'precio_apertura': float(last_row['Open']),
                            'precio_max_dia': float(last_row['High']),
                            'precio_min_dia': float(last_row['Low']),
                            'volumen': int(last_row['Volume']),
                            'cambio_porcentaje': info.get('regularMarketChangePercent', 0),
                            'moneda': info.get('currency', 'USD')
                        })
                except Exception as e:
                    print(f"Error con {simbolo}: {e}")
                    continue
            
            return resultados
        
        except Exception as e:
            print(f"Error obteniendo múltiples precios: {e}")
            return []
    
    @staticmethod
    def obtener_historico(simbolo, periodo='1mo'):
        """
        Obtener datos históricos de una acción
        Periodos válidos: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            ticker = yf.Ticker(simbolo)
            hist = ticker.history(period=periodo)
            
            if hist.empty:
                return None
            
            # Convertir a formato JSON serializable
            datos = []
            for index, row in hist.iterrows():
                datos.append({
                    'fecha': index.strftime('%Y-%m-%d'),
                    'apertura': float(row['Open']),
                    'maximo': float(row['High']),
                    'minimo': float(row['Low']),
                    'cierre': float(row['Close']),
                    'volumen': int(row['Volume'])
                })
            
            return datos
        
        except Exception as e:
            print(f"Error obteniendo histórico de {simbolo}: {e}")
            return None
    
    @staticmethod
    def buscar_accion(query):
        """Buscar acciones por nombre o símbolo"""
        try:
            # Nota: yfinance no tiene búsqueda directa
            # Esto es una implementación simplificada
            # En producción se usaría una API específica de búsqueda
            
            ticker = yf.Ticker(query)
            info = ticker.info
            
            if info.get('symbol'):
                return [{
                    'simbolo': info['symbol'],
                    'nombre': info.get('longName', info['symbol']),
                    'sector': info.get('sector'),
                    'industria': info.get('industry'),
                    'mercado': info.get('exchange')
                }]
            
            return []
        
        except Exception as e:
            print(f"Error buscando {query}: {e}")
            return []
    
    @staticmethod
    def obtener_acciones_populares():
        """Obtener lista de acciones más populares"""
        simbolos_populares = [
            'AAPL',  # Apple
            'MSFT',  # Microsoft
            'GOOGL', # Google
            'AMZN',  # Amazon
            'TSLA',  # Tesla
            'META',  # Meta (Facebook)
            'NVDA',  # NVIDIA
            'JPM',   # JP Morgan
            'V',     # Visa
            'WMT',   # Walmart
            'NFLX',  # Netflix
            'DIS',   # Disney
            'PYPL',  # PayPal
            'INTC',  # Intel
            'AMD'    # AMD
        ]
        
        return StockService.obtener_multiples_precios(simbolos_populares)
