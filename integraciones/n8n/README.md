# Integración n8n con sistema de gestión financiera

Este directorio contiene workflows de ejemplo para n8n que se integran con la API del sistema de gestión financiera.

## Workflows disponibles

### 1. Monitor de transacciones grandes

**Archivo**: [workflow-monitor-transacciones.json](workflow-monitor-transacciones.json)

**Descripción**: monitorea transacciones cada 5 minutos y envía alertas cuando hay transacciones mayores a 1000 USD.

**Nodos utilizados**:
- Schedule Trigger (cada 5 minutos)
- HTTP Request (GET /api/transactions)
- Function (filtrar transacciones superiores a 1000 USD)
- IF (verificar si hay alertas)
- Webhook/Email/Slack (notificación)

**Configuración**:
1. Importar el workflow en n8n
2. Configurar credenciales de autenticación (Header Auth con X-API-Key)
3. Configurar el nodo de notificación (Slack o correo electrónico)
4. Activar el workflow

### 2. Reporte diario automatizado

**Archivo**: [workflow-reporte-diario.json](workflow-reporte-diario.json)

**Descripción**: genera un reporte diario de transacciones a las 23:00 y lo envía por correo electrónico.

**Nodos utilizados**:
- Cron Trigger (diario a las 23:00)
- HTTP Request (GET /api/reports/daily)
- Function (formatear datos)
- Email/Google Sheets (envío o almacenamiento)

### 3. Sincronización con Google Sheets

**Descripción**: cada hora, obtiene las transacciones nuevas y las agrega a Google Sheets.

**Nodos utilizados**:
- Schedule Trigger (cada hora)
- HTTP Request (GET /api/transactions)
- Google Sheets - Get Values (verificar última fila)
- Function (filtrar nuevas transacciones)
- Google Sheets - Append (agregar filas)

## Instrucciones de importación

### Paso 1: instalar n8n

**Opción A - Docker (recomendado)**:
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Opción B - npm**:
```bash
npm install n8n -g
n8n start
```

### Paso 2: importar workflows

1. Abrir n8n en `http://localhost:5678`
2. Hacer clic en el botón "Import from File"
3. Seleccionar el archivo JSON del workflow
4. Hacer clic en "Import"

### Paso 3: configurar credenciales

#### Autenticación API

1. Hacer clic en "Credentials" → "New"
2. Seleccionar "Header Auth"
3. Configurar:
   - **Name**: API Financiera Auth
   - **Name**: X-API-Key
   - **Value**: api_key_demo_12345

#### URL de la API

Si n8n está en Docker, usar: `http://host.docker.internal:5000/api`  
Si n8n está en local, usar: `http://localhost:5000/api`

### Paso 4: probar workflow

1. Hacer clic en "Execute Workflow"
2. Verificar resultados en cada nodo
3. Ajustar según necesidades

### Paso 5: activar workflow

1. Activar el toggle "Active" en la esquina superior derecha
2. El workflow se ejecutará automáticamente

## Personalización

### Cambiar frecuencia de ejecución

En el nodo Schedule Trigger:
```javascript
// Cada 5 minutos
Minutes Between Triggers: 5

// Cada hora
Hours Between Triggers: 1

// Diario a las 9:00
Trigger at: 09:00
```

### Cambiar umbral de alerta

En el nodo Function de filtrado:
```javascript
// Cambiar 1000 por el monto deseado
const umbral = 1000;

const grandesTransacciones = items[0].json.data.filter(tx => {
  return parseFloat(tx.monto) > umbral;
});

return grandesTransacciones.map(tx => ({json: tx}));
```

### Agregar más filtros

```javascript
// Filtrar por moneda y monto
const transaccionesFiltradas = items[0].json.data.filter(tx => {
  return parseFloat(tx.monto) > 1000 && tx.moneda === 'EUR';
});

// Filtrar por estado
const completadas = items[0].json.data.filter(tx => {
  return tx.estado === 'completed';
});

// Filtrar por fecha
const hoy = new Date();
const transaccionesHoy = items[0].json.data.filter(tx => {
  const fechaTx = new Date(tx.fecha);
  return fechaTx.toDateString() === hoy.toDateString();
});
```

## Solución de problemas

### Error de conexión

**Problema**: n8n no puede conectarse a la API.

**Solución**:
- Verificar que la API esté ejecutándose
- Si n8n está en Docker, usar `host.docker.internal` en lugar de `localhost`
- Verificar que la API Key sea correcta

### Error de autenticación

**Problema**: respuesta 401 Unauthorized.

**Solución**:
- Verificar credenciales en n8n
- Asegurarse de que el header sea exactamente `X-API-Key`
- Verificar que el valor de la API Key sea correcto

### Workflow no se activa

**Problema**: el workflow programado no se ejecuta.

**Solución**:
- Verificar que el workflow esté activado (toggle en ON)
- Revisar la configuración del Schedule Trigger
- Consultar los logs de n8n para errores

## Características avanzadas

### Variables de entorno

Almacenar configuración sensible en variables de entorno:

```bash
export N8N_API_KEY="api_key_demo_12345"
export N8N_API_URL="http://localhost:5000/api"
```

Luego usar en n8n: `{{$env.N8N_API_KEY}}`

### Webhooks

Configurar webhook para triggers en tiempo real:

1. Agregar nodo "Webhook"
2. Configurar método HTTP (POST)
3. Copiar URL del webhook
4. Configurar la API para enviar eventos a esa URL

### Error handling

Agregar nodos de manejo de errores:

1. Hacer clic derecho en el nodo
2. Seleccionar "Add Error Trigger"
3. Configurar acción alternativa

## Recursos adicionales

- [Documentación oficial de n8n](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [API de referencia del sistema](../../README.md)


### Error: "Connection refused"

**Causa**: n8n no puede conectarse a la API

**Solución**:
- Si n8n está en Docker, usar `host.docker.internal` en lugar de `localhost`
- Verificar que la API esté corriendo: `http://localhost:5000/api/health`

### Error: "401 Unauthorized"

**Causa**: API key incorrecta

**Solución**:
- Verificar que el header `X-API-Key` esté configurado
- Verificar que el valor sea `api_key_demo_12345`

### No se ejecuta el workflow

**Causa**: Workflow no está activado

**Solución**:
- Click en el toggle "Active" en la esquina superior derecha
- Verificar que el trigger esté configurado correctamente

## Ejemplos de código para nodos Function

### Formatear datos para email

```javascript
const data = items[0].json;

const html = `
<h2>Reporte Diario - ${data.fecha}</h2>
<p><strong>Total transacciones:</strong> ${data.total_transacciones}</p>
<p><strong>Monto total:</strong> $${data.monto_total}</p>
<p><strong>Promedio:</strong> $${data.monto_promedio}</p>
<p><strong>Máxima:</strong> $${data.transaccion_maxima}</p>
`;

return [{
  json: {
    subject: `Reporte Diario - ${data.fecha}`,
    html: html,
    to: 'tu-email@ejemplo.com'
  }
}];
```

### Detectar anomalías

```javascript
const transacciones = items[0].json.data;

// Calcular promedio
const montos = transacciones.map(tx => parseFloat(tx.monto));
const promedio = montos.reduce((a, b) => a + b, 0) / montos.length;
const desviacion = Math.sqrt(
  montos.map(x => Math.pow(x - promedio, 2))
    .reduce((a, b) => a + b) / montos.length
);

// Detectar valores atípicos (> 2 desviaciones estándar)
const anomalias = transacciones.filter(tx => {
  return Math.abs(parseFloat(tx.monto) - promedio) > (2 * desviacion);
});

return anomalias.map(tx => ({ json: tx }));
```

## Recursos adicionales

- [Documentación oficial de n8n](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Ejemplos de workflows](https://n8n.io/workflows/)
