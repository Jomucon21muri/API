# Sistema de gestión financiera - API REST y Dashboard

## Resumen ejecutivo

Sistema completo de gestión financiera desarrollado en Python con Flask, que incluye API REST, dashboard web interactivo y módulos de automatización. El proyecto implementa gestión de clientes, transacciones, portafolios de inversión y análisis de mercado de valores.

## Inicio rápido

### Ejecución del sistema (menos de 2 minutos)

**Linux/macOS:**
```bash
./start.sh
```

**Windows PowerShell:**
```powershell
.\start_dashboard.ps1
```

**Manual (dos terminales):**

Terminal 1 - Servidor de API:
```bash
cd api
python3 app.py
```

Terminal 2 - Servidor web del dashboard:
```bash
python3 -m http.server 8080
```

### Acceso a los componentes

- **Dashboard**: http://localhost:8080
- **API**: http://localhost:5000
- **Verificación de estado**: http://localhost:5000/api/health

### Configuración inicial del dashboard

En la sección Settings, configurar:

- **URL base de la API**: http://localhost:5000/api
- **Clave de autenticación**: api_key_demo_12345

Utilizar "Test Connection" para validar la conectividad.

### Datos de demostración incluidos

- 40 clientes en 11 países
- 368 transacciones financieras
- 160 posiciones de portafolio
- 15 acciones del mercado con datos actualizados


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

**Paso 4: configurar variables de entorno**

Crear archivo .env en la carpeta api/:

```
FLASK_ENV=development
SECRET_KEY=clave_secreta_personalizada
DATABASE_URL=sqlite:///financial.db
API_KEY=api_key_demo_12345
```

**Paso 5: inicializar base de datos**

```bash
cd ..
python scripts/populate_db.py
```

Este comando ejecuta:
- Creación de esquema de base de datos
- Población con datos de ejemplo
- Verificación de integridad

**Paso 6: iniciar el sistema**

Opción recomendada (dos terminales):

Terminal 1 - Iniciar la API:
```bash
cd api
python3 app.py
```

La API estará disponible en http://localhost:5000

Terminal 2 - Iniciar servidor web para el dashboard:
```bash
python3 -m http.server 8080
```

El dashboard estará disponible en http://localhost:8080

Opción alternativa (Windows con PowerShell):
```powershell
.\start_dashboard.ps1
```

### Verificación de instalación

Para verificar que el sistema funciona correctamente:

1. Verificar que la API responde:
   ```bash
   curl http://localhost:5000/api/health
   ```
   Debe responder con estado "ok" y "database: connected"

2. Abrir el dashboard en el navegador:
   - Navegar a http://localhost:8080
   - O abrir directamente index.html (puede presentar problemas con CORS)

3. En el dashboard, ir a la sección "Settings" (Configuración):
   - Verificar que la URL de API sea: http://localhost:5000/api
   - Verificar que la API Key sea: api_key_demo_12345
   - Hacer clic en "Test Connection"
   - Debe mostrar "Conexión exitosa"

4. Explorar las diferentes secciones del dashboard:
   - Overview: estadísticas generales
   - Customers: listado de clientes (40 registros)
   - Transactions: transacciones (368 registros)
   - Portfolio: carteras de inversión

## Uso del sistema

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
- Métricas de valor total, ganancia o pérdida y rendimiento
- Lista detallada de posiciones en acciones

### Actualización de datos

Los datos del dashboard se cargan mediante llamadas a la API REST. Para actualizar la información, utilizar el botón "Recargar" disponible en cada sección.

## Solución de problemas

### Problema: el dashboard muestra "Desconectado" o "Failed to fetch"

**Diagnóstico:**
Este error indica que el dashboard no puede conectarse a la API.

**Soluciones:**

1. **Verificar que la API esté ejecutándose:**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Si no responde, iniciar la API:
   ```bash
   cd api
   python3 app.py
   ```

2. **Verificar acceso al dashboard desde servidor HTTP:**
   - Correcto: http://localhost:8080 (usando python3 -m http.server 8080)
   - Incorrecto: file:///ruta/al/index.html (causará errores CORS)

3. **Verificar configuración en el dashboard:**
   - Ir a Settings (Configuración)
   - URL de API: http://localhost:5000/api
   - API Key: api_key_demo_12345
   - Hacer clic en "Test Connection"

4. **Revisar consola del navegador (F12):**
   - Errores CORS: no se está usando un servidor HTTP
   - Errores de red: la API no está en ejecución
   - Error 401: API Key incorrecta

5. **Si se trabaja en un Codespace o entorno remoto:**
   - El dashboard detecta automáticamente la URL correcta
   - Asegurar que los puertos 5000 y 8080 estén públicamente accesibles
   - Verificar que los puertos estén reenviados correctamente

### Problema: error al cargar datos

**Solución:**
1. Verificar que la base de datos esté inicializada:
   ```bash
   ls -lh api/instance/financial.db
   ```
2. Si no existe, inicializar con:
   ```bash
   python scripts/populate_db.py
   ```
3. Verificar logs de la API en la terminal donde se ejecuta

### Problema: dependencias no instaladas

**Solución:**
```bash
cd api
pip install -r requirements.txt
```

### Problema: puerto 5000 ocupado

**Solución:**
1. Identificar el proceso:
   ```bash
   lsof -i :5000
   ```
2. Detener el proceso o cambiar el puerto en api/app.py

## Documentación técnica

Sistema de gestión financiera - Versión 1.0  
Última actualización: mayo de 2026

## Contribuciones

Este repositorio es de uso educativo como apoyo a clases. No se aceptan contribuciones externas.

## Licencia

Material educativo desarrollado con fines académicos.
