# Dashboard API - GitHub Pages

Un dashboard moderno e interactivo con chatbot integrado, diseñado para GitHub Pages.

## 🚀 Características

- **Diseño Responsive**: Adaptable a cualquier dispositivo (móvil, tablet, desktop)
- **Chatbot Integrado**: Asistente virtual que responde preguntas frecuentes
- **Estadísticas en Tiempo Real**: Visualización dinámica de métricas
- **Navegación Suave**: Transiciones fluidas entre secciones
- **Enlace a Web Principal**: Botón directo a tu sitio web principal

## 📦 Contenido

- `index.html` - Página principal del dashboard
- `style.css` - Estilos CSS modernos y responsive
- `script.js` - Funcionalidad del chatbot y animaciones
- `README.md` - Este archivo

## 🌐 Configurar GitHub Pages

### Opción 1: Desde la configuración del repositorio

1. Ve a tu repositorio en GitHub
2. Click en **Settings** (Configuración)
3. En el menú lateral, click en **Pages**
4. En **Source** (Fuente), selecciona la rama `main`
5. Selecciona la carpeta `/ (root)`
6. Click en **Save** (Guardar)
7. Espera unos minutos y tu sitio estará disponible en: `https://Jomucon21muri.github.io/API/`

### Opción 2: Usando GitHub Actions (automático)

El sitio se despliega automáticamente cuando haces push a la rama `main`.

## ⚙️ Personalización

### Cambiar la URL de tu web principal

1. Abre `index.html`
2. Busca todas las instancias de `https://tuempresa.com`
3. Reemplázalas con la URL de tu sitio web

```html
<!-- Ejemplo -->
<a href="https://tu-sitio-web.com" target="_blank" class="btn-primary">
```

### Personalizar el nombre del dashboard

En `index.html`, modifica:
- `<title>` en el `<head>`
- El logo en la navbar
- El título en la sección hero

### Personalizar los colores

En `style.css`, modifica las variables CSS:

```css
:root {
    --primary-color: #6366f1;  /* Color principal */
    --secondary-color: #8b5cf6; /* Color secundario */
    /* ... otros colores */
}
```

### Personalizar el chatbot

En `script.js`, modifica el objeto `botResponses`:

```javascript
const botResponses = {
    'hola': 'Tu respuesta personalizada',
    'ayuda': 'Tu mensaje de ayuda',
    // Añade más respuestas...
};
```

## 🤖 Funcionalidades del Chatbot

El chatbot puede responder a:
- Saludos (hola, buenos días)
- Preguntas sobre servicios
- Información de contacto
- Preguntas sobre la API
- Soporte técnico
- Y más...

## 📱 Responsive Design

El dashboard está optimizado para:
- 📱 Móviles (< 768px)
- 💻 Tablets (768px - 1024px)
- 🖥️ Desktop (> 1024px)

## 🎨 Iconos

Utilizamos **Font Awesome 6.4.0** para todos los iconos. Puedes añadir más desde: https://fontawesome.com/icons

## 🔧 Mantenimiento

### Actualizar estadísticas

Las estadísticas se actualizan automáticamente en `script.js`. Para cambiar los valores iniciales, modifica el HTML en `index.html`:

```html
<h3 id="users-count">1,234</h3>
```

### Añadir nuevas secciones

1. Añade la sección en `index.html`
2. Añade el enlace en la navbar
3. Añade estilos en `style.css`

## 📄 Estructura del Proyecto

```
API/
├── index.html      # Página principal
├── style.css       # Estilos
├── script.js       # JavaScript
└── README.md       # Documentación
    ├── test_api.py                    # Scripts de prueba
    └── populate_db.py                 # Poblar base de datos
```

## Tecnologías utilizadas

- **Backend**: Python 3.9+ con Flask
- **Base de datos**: SQLite (fácil de configurar) / PostgreSQL (producción)
- **Frontend**: Dashboard HTML/CSS/JS con diseño UX/UI en escala de grises
- **Bot de Telegram**: Reportes y gestión vía Telegram
- **Automatización**: n8n, Make, Zapier
- **APIs externas**: Stripe (pagos), Exchange Rate API (tipos de cambio)

## Documentación

### 📘 Para aprender

- **[Tutorial interactivo (Jupyter Notebook)](tutorial-api-completo.ipynb)**: Explicación detallada de cada función, con ejemplos ejecutables paso a paso
- **[Guía paso a paso](docs/guia-paso-a-paso.md)**: Instrucciones completas para construir la API desde cero

### 🚀 Para implementar

- **[Inicio rápido (5 minutos)](QUICKSTART.md)**: Ejecuta la API en 5 minutos
- **[Dashboard visual](DASHBOARD_README.md)**: Interfaz gráfica para visualizar y gestionar datos
- **[Integración completa](docs/integracion-completa.md)**: Flujos end-to-end reales con n8n, Make y Zapier

### 🔌 Integraciones

- **[Bot de Telegram](telegram_bot/README.md)**: Bot para reportes y gestión de transacciones
  - **[Inicio rápido del bot](telegram_bot/QUICKSTART.md)**: Configura tu bot en 5 minutos
  - **[Guía completa del bot](docs/bot-telegram-paso-a-paso.md)**: Paso a paso detallado
- **[n8n](integraciones/n8n/README.md)**: Workflows para alertas y reportes
- **[Make](integraciones/make/README.md)**: Escenarios de sincronización
- **[Zapier](integraciones/zapier/README.md)**: Zaps para automatización

## Inicio rápido
### Opción 1: inicio automático con dashboard (recomendado)

```powershell
# Ejecutar script de inicio automático
.\start_dashboard.ps1
```

Este script:
- ✓ Inicia la API automáticamente
- ✓ Abre el dashboard en el navegador
- ✓ Configura todo lo necesario

### Opción 2: inicio manual

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
cd api
pip install -r requirements.txt

# 3. Configurar base de datos
python scripts/populate_db.py

# 4. Ejecutar API
python app.py

# 5. Abrir dashboard
# Hacer doble clic en dashboard.html o abrirlo en el navegador
```

La API estará disponible en `http://localhost:5000`  
El dashboard en `dashboard.html` (se abre automáticamente)

Ver [QUICKSTART.md](QUICKSTART.md) para más detalles o [DASHBOARD_README.md](DASHBOARD_README.md) para la guía completa del dashboard.
La API estará disponible en `http://localhost:5000`

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Verificar estado de la API |
| GET | `/api/transactions` | Listar transacciones |
| POST | `/api/transactions` | Crear transacción |
| GET | `/api/customers` | Listar clientes |
| POST | `/api/customers` | Crear cliente |
| GET | `/api/reports/daily` | Reporte diario |
| GET | `/api/exchange-rate/{currency}` | Tipo de cambio |
Bot de Telegram para reportes y gestión
Consulta reportes, transacciones y clientes directamente desde Telegram.
- Ver [telegram_bot/QUICKSTART.md](telegram_bot/QUICKSTART.md) para inicio rápido
- Ver [docs/bot-telegram-paso-a-paso.md](docs/bot-telegram-paso-a-paso.md) para guía completa

### 2. Sistema de alertas de transacciones (n8n)
Monitorea transacciones grandes y envía notificaciones automáticas.

### 3. Sincronización con Google Sheets (Make)
Sincroniza automáticamente transacciones con hojas de cálculo.

### 4. Sincronización con Google Sheets (Make)
Sincroniza automáticamente transacciones con hojas de cálculo.

### 3. Backup automático (Zapier)
Realiza backups diarios de transacciones a múltiples destinos.

## Seguridad

La API implementa:
- Autenticación mediante API Keys
- Rate limiting
- Validación de datos
- Logging de auditoría

## Soporte

Para preguntas sobre este proyecto, consultar la documentación del curso o abrir un issue.
