# Dashboard API - Sistema de visualización y gestión de datos financieros

## Resumen ejecutivo

Este proyecto implementa un sistema completo de gestión financiera compuesto por una API REST desarrollada en Python con Flask, un dashboard web interactivo, y módulos de automatización mediante herramientas de terceros. El sistema está diseñado para desplegarse en GitHub Pages, proporcionando acceso web público al panel de control.

## Índice

1. [Descripción general](#descripción-general)
2. [Arquitectura del sistema](#arquitectura-del-sistema)
3. [Componentes principales](#componentes-principales)
4. [Instalación y configuración](#instalación-y-configuración)
5. [Uso del sistema](#uso-del-sistema)
6. [Configuración de GitHub Pages](#configuración-de-github-pages)
7. [Personalización](#personalización)
8. [Estructura del proyecto](#estructura-del-proyecto)
9. [Tecnologías utilizadas](#tecnologías-utilizadas)
10. [Documentación técnica](#documentación-técnica)

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

## Uso del sistema

### Acceso al dashboard

**Método 1: GitHub Pages**

Una vez configurado GitHub Pages, acceder a:
https://jomucon21muri.github.io/API/

**Método 2: Local**

Abrir directamente el archivo index.html en un navegador web.

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

## Configuración de GitHub Pages

### Procedimiento de activación

**Paso 1: Acceder a configuración del repositorio**

1. Navegar a https://github.com/Jomucon21muri/API
2. Hacer clic en "Settings" (Configuración)

**Paso 2: Configurar GitHub Pages**

1. En el menú lateral, seleccionar "Pages"
2. En la sección "Source":
   - Branch: Seleccionar "main"
   - Folder: Seleccionar "/ (root)"
3. Hacer clic en "Save"

**Paso 3: Verificar despliegue**

- El proceso de despliegue tarda aproximadamente 2-5 minutos
- Un indicador verde aparecerá cuando el sitio esté publicado
- URL del sitio: https://jomucon21muri.github.io/API/

### Archivos de configuración

El proyecto incluye los siguientes archivos para optimizar GitHub Pages:

- **.nojekyll**: Deshabilita el procesamiento Jekyll
- **_config.yml**: Configuración del tema y metadatos
- **404.html**: Página de error personalizada
- **index.html**: Página principal del dashboard

### Actualización del sitio

Para actualizar el contenido publicado:

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

GitHub Pages se actualizará automáticamente en 1-2 minutos.

## Personalización

### Personalización de colores

Los colores del dashboard se definen mediante variables CSS en la sección <style> del archivo index.html:

```css
:root {
    --bg-primary: #f5f5f5;      /* Fondo principal */
    --bg-secondary: #ffffff;     /* Fondo secundario */
    --text-primary: #212121;     /* Texto principal */
    --text-secondary: #616161;   /* Texto secundario */
    --active-bg: #424242;        /* Fondo activo */
}
```

### Configuración de la API

Para conectar el dashboard con la API:

1. Abrir la sección "Settings" en el dashboard
2. Configurar la URL base de la API (por defecto: http://localhost:5000/api)
3. Establecer la API Key de autenticación
4. Probar la conexión con el botón "Test Connection"

### Modificación de datos de ejemplo

Para cambiar los datos precargados en la base de datos, editar el archivo scripts/populate_db.py y ejecutar:

```bash
python scripts/populate_db.py
```

## Estructura del proyecto

```
API/
├── index.html                      # Dashboard principal (interfaz financiera)
├── 404.html                        # Página de error personalizada
├── .nojekyll                       # Configuración GitHub Pages
├── _config.yml                     # Configuración Jekyll
├── README.md                       # Documentación principal
├── api/                            # Backend API
│   ├── app.py                      # Aplicación Flask principal
│   ├── models.py                   # Modelos de base de datos
│   ├── routes.py                   # Definición de endpoints
│   ├── config.py                   # Configuración del sistema
│   ├── requirements.txt            # Dependencias Python
│   ├── workflow_service.py         # Servicios de automatización
│   └── stock_service.py            # Servicios de acciones
├── database/                       # Base de datos
│   ├── schema.sql                  # Esquema de tablas
│   ├── seed_data.sql               # Datos iniciales
│   └── queries.sql                 # Consultas predefinidas
├── scripts/                        # Scripts de utilidad
│   ├── populate_db.py              # Población de base de datos
│   └── test_api.py                 # Pruebas de API
├── docs/                           # Documentación adicional
│   ├── guia-paso-a-paso.md         # Tutorial detallado
│   ├── integracion-completa.md     # Guía de integraciones
│   └── bot-telegram-paso-a-paso.md # Configuración de bot
├── telegram_bot/                   # Bot de Telegram
│   ├── bot.py                      # Lógica del bot
│   ├── requirements.txt            # Dependencias
│   └── README.md                   # Documentación
└── integraciones/                  # Módulos de automatización
    ├── n8n/                        # Workflows n8n
    ├── make/                       # Escenarios Make
    └── zapier/                     # Zaps de Zapier
```

## Tecnologías utilizadas

### Backend

- **Python 3.9+**: Lenguaje de programación principal
- **Flask**: Framework web para la API REST
- **SQLAlchemy**: ORM para gestión de base de datos
- **SQLite**: Base de datos para desarrollo
- **PostgreSQL**: Base de datos para producción (opcional)

### Frontend

- **HTML5**: Estructura del dashboard
- **CSS3**: Estilos y diseño responsive
- **JavaScript**: Lógica de interacción con la API y actualización de datos

### Herramientas de desarrollo

- **Git**: Control de versiones
- **GitHub Pages**: Hosting del dashboard
- **VS Code**: Editor de código recomendado
- **Postman**: Pruebas de API (opcional)

### Integraciones

- **n8n**: Automatización de workflows
- **Make (Integromat)**: Escenarios de integración
- **Zapier**: Automatización de tareas
- **Telegram Bot API**: Bot de mensajería

## Documentación técnica

### Especificación de la API

Todos los endpoints de la API siguen el estándar RESTful y retornan respuestas en formato JSON.

**Formato de respuesta exitosa:**
```json
{
    "status": "success",
    "data": {
        // Datos solicitados
    }
}
```

**Formato de respuesta de error:**
```json
{
    "status": "error",
    "message": "Descripción del error"
}
```

### Autenticación

La API utiliza autenticación mediante API Key en el header:

```
Authorization: Bearer api_key_demo_12345
```

### Códigos de respuesta HTTP

- 200: Operación exitosa
- 201: Recurso creado exitosamente
- 400: Solicitud incorrecta
- 401: No autorizado
- 404: Recurso no encontrado
- 500: Error interno del servidor

### Ejemplos de uso de la API

**Listar clientes:**
```bash
curl -X GET http://localhost:5000/api/customers \
  -H "Authorization: Bearer api_key_demo_12345"
```

**Crear transacción:**
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Authorization: Bearer api_key_demo_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "amount": 100.50,
    "currency": "EUR",
    "type": "payment"
  }'
```

**Consultar portfolio:**
```bash
curl -X GET http://localhost:5000/api/portfolio/customer/1 \
  -H "Authorization: Bearer api_key_demo_12345"
```

### Solución de problemas comunes

**Problema: El dashboard muestra "Desconectado"**

Solución:
1. Verificar que la API esté ejecutándose en http://localhost:5000
2. Comprobar la configuración de URL y API Key en el dashboard
3. Revisar la consola del navegador (F12) para errores

**Problema: Error al cargar datos**

Solución:
1. Verificar que la base de datos esté inicializada
2. Ejecutar: python scripts/populate_db.py
3. Comprobar los logs de la API

**Problema: GitHub Pages no muestra el sitio**

Solución:
1. Esperar 5 minutos después de activar Pages
2. Verificar configuración: rama main, carpeta / (root)
3. Limpiar caché del navegador (Ctrl+F5)

### Mantenimiento y actualizaciones

**Actualización de dependencias:**
```bash
pip install --upgrade -r requirements.txt
```

**Backup de base de datos:**
```bash
cp api/financial.db api/financial.db.backup
```

**Verificación de estado del sistema:**
```bash
curl http://localhost:5000/api/health
```

## Información de contacto

Para soporte técnico o consultas sobre el proyecto:

- Repositorio: https://github.com/Jomucon21muri/API
- Issues: https://github.com/Jomucon21muri/API/issues
- Dashboard en producción: https://jomucon21muri.github.io/API/

---

Documentación técnica - Versión 1.0
Última actualización: Mayo 2026
