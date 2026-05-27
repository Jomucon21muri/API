# Dashboard API - Sistema de visualización y gestión de datos financieros

## Resumen ejecutivo

Este proyecto implementa un sistema completo de gestión financiera compuesto por una API REST desarrollada en Python con Flask, un dashboard web interactivo, y módulos de automatización mediante herramientas de terceros. El sistema está diseñado para desplegarse en GitHub Pages, proporcionando acceso web público al panel de control.


## Descripción general

El proyecto consiste en una solución integral para la gestión de datos financieros que incluye:

- **API REST**: Interfaz de programación para gestión de clientes, transacciones, acciones y portfolios
- **Base de datos**: Sistema de almacenamiento con 40 clientes, 368 transacciones y 160 posiciones de portfolio
- **Dashboard web**: Interfaz gráfica responsive con visualización de datos en tiempo real
- **Módulos de automatización**: Integración con n8n, Make y Zapier

### Estado actual del sistema

El sistema se encuentra completamente funcional con las siguientes características:

**Base de datos poblada:**
- 40 clientes distribuidos en 11 países (España, México, Estados Unidos, Francia, Alemania, Italia, Argentina, Colombia, Brasil, Reino Unido, Canadá)
- 368 transacciones con múltiples tipos (pago, reembolso, transferencia, suscripción, compra)
- 15 acciones del mercado con datos actualizados (AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, JPM, V, WMT, NFLX, DIS, PYPL, INTC, AMD)
- 160 posiciones activas de portfolio (100% de cobertura de clientes)

**Endpoints disponibles:** 21 endpoints RESTful completamente funcionales

## Arquitectura del sistema

### Componentes técnicos

El sistema sigue una arquitectura de tres capas:

1. **Capa de presentación**: Dashboard HTML/CSS/JavaScript con diseño responsive
2. **Capa de lógica de negocio**: API REST desarrollada en Flask
3. **Capa de datos**: Base de datos SQLite (desarrollo) / PostgreSQL (producción)

### Flujo de datos

```
Usuario → Dashboard web → API REST → Base de datos
```

## Componentes principales

### Dashboard web

Interfaz gráfica moderna con las siguientes características:

**Diseño responsive:**
- Adaptable a dispositivos móviles (< 768px)
- Optimizado para tablets (768px - 1024px)
- Diseño completo para escritorio (> 1024px)

**Secciones principales:**
1. Resumen general (Overview): Estadísticas clave y métricas del sistema
2. Gestión de clientes (Customers): Visualización y administración de clientes
3. Transacciones (Transactions): Historial de operaciones financieras
4. Portfolio: Gestión de carteras de inversión
5. Estadísticas globales (Stats): Análisis de datos agregados
6. Workflows: Estado de integraciones y automatizaciones
7. Configuración (Settings): Parámetros de conexión y autenticación

**Navegación:**
- Sistema de navegación suave entre secciones
- Indicador visual de sección activa
- Menú adaptativo para dispositivos móviles

### API REST

Sistema backend con los siguientes grupos de endpoints:

**Gestión de clientes (4 endpoints):**
- GET /api/customers: Listado con filtros y paginación
- POST /api/customers: Creación de nuevos clientes
- PUT /api/customers/<id>: Actualización de datos
- DELETE /api/customers/<id>: Eliminación lógica

**Gestión de transacciones (2 endpoints):**
- GET /api/transactions: Consulta con filtros múltiples
- POST /api/transactions: Registro de nuevas transacciones

**Gestión de acciones (5 endpoints):**
- GET /api/stocks: Listado completo de acciones
- GET /api/stocks/<simbolo>: Detalles específicos
- GET /api/stocks/<simbolo>/historico: Datos históricos
- GET /api/stocks/populares: Ranking de popularidad
- POST /api/stocks/actualizar-multiples: Actualización masiva

**Gestión de portfolio (5 endpoints):**
- GET /api/portfolio: Todas las posiciones
- GET /api/portfolio/customer/<id>: Portfolio por cliente
- POST /api/portfolio: Creación de posiciones
- DELETE /api/portfolio/<id>: Eliminación de posiciones
- PATCH /api/portfolio/<id>: Actualización de cantidades

**Estadísticas y sistema (4 endpoints):**
- GET /api/stats/global: Métricas globales del sistema
- GET /api/workflows: Estado de automatizaciones
- GET /api/health: Verificación de estado del sistema
- OPTIONS /api/*: Soporte CORS

## Instalación y configuración

### Requisitos previos

El sistema requiere las siguientes dependencias:

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Git (control de versiones)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Instalación paso a paso

**Paso 1: Clonar el repositorio**

```bash
git clone https://github.com/Jomucon21muri/API.git
cd API
```

**Paso 2: Crear entorno virtual**

Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Paso 3: Instalar dependencias**

```bash
cd api
pip install -r requirements.txt
```

Las dependencias principales incluyen:
- Flask: Framework web
- SQLAlchemy: ORM para base de datos
- Flask-CORS: Soporte para CORS
- python-dotenv: Gestión de variables de entorno

**Paso 4: Configurar variables de entorno**

Crear archivo .env en la carpeta api/:

```
FLASK_ENV=development
SECRET_KEY=clave_secreta_personalizada
DATABASE_URL=sqlite:///financial.db
API_KEY=api_key_demo_12345
```

**Paso 5: Inicializar base de datos**

```bash
cd ..
python scripts/populate_db.py
```

Este comando ejecuta:
- Creación de esquema de base de datos
- Población con datos de ejemplo
- Verificación de integridad

**Paso 6: Iniciar el sistema**

Opción automática (Windows):
```powershell
.\start_dashboard.ps1
```

Opción manual:
```bash
cd api
python app.py
```

El sistema estará disponible en http://localhost:5000

### Verificación de instalación

Para verificar que el sistema funciona correctamente:

1. Acceder a http://localhost:5000/api/health
2. El sistema debe responder con estado "healthy"
3. Abrir dashboard.html en el navegador
4. Verificar conexión con la API desde la sección Configuración



### Navegación por secciones

**Sección de inicio:**
Presenta un resumen general del sistema con:
- Título y descripción del proyecto
- Botones de acceso rápido
- Enlaces a la web principal

**Gestión de clientes:**
- Tabla completa de clientes registrados
- Filtros por país y estado
- Exportación de datos

**Gestión de transacciones:**
- Visualización de todas las transacciones
- Filtros por estado, tipo y cliente
- Detalles de montos y fechas

**Gestión de portfolio:**
- Selector de cliente para visualización individual
- Métricas de valor total, ganancia/pérdida y rendimiento
- Lista detallada de posiciones en acciones

### Actualización de datos

Los datos del dashboard se cargan mediante llamadas a la API REST. Para actualizar la información, utilizar el botón "Recargar" disponible en cada sección.


Documentación técnica - Versión 1.0
Última actualización: Mayo 2026
