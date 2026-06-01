# Integración Zapier con sistema de gestión financiera

Este directorio contiene ejemplos de Zaps que se integran con la API del sistema de gestión financiera.

## Zaps disponibles

### 1. Copia de seguridad diaria a Google Drive

**Descripción**: cada día a las 23:00, obtiene el reporte diario y lo guarda en múltiples destinos.

**Trigger**: Schedule by Zapier (Daily 23:00)

**Actions**:
1. Webhooks - GET daily report
2. Google Sheets - Create row
3. Dropbox - Upload file
4. Email - Send notification

### 2. Notificaciones de transacciones grandes

**Descripción**: usa webhook para recibir notificaciones en tiempo real de transacciones superiores a 1000 USD.

**Trigger**: Webhooks by Zapier (Catch Hook)

**Actions**:
1. Filter - Solo transacciones superiores a 1000 USD
2. Slack - Send message
3. Email - Send email
4. Trello - Create card

### 3. Conciliación bancaria

**Descripción**: compara transacciones de la API con extracto bancario.

**Trigger**: Gmail - New Attachment (extracto bancario)

**Actions**:
1. Formatter - Parse CSV
2. Webhooks - GET API transactions
3. Code - Compare transactions
4. Google Sheets - Log discrepancies
5. Email - Send report

## Configuración básica

### Paso 1: crear cuenta en Zapier

1. Visitar [zapier.com](https://zapier.com)
2. Registrarse (plan gratuito: 100 tareas mensuales)
3. Verificar dirección de correo electrónico

### Paso 2: crear un Zap

1. Hacer clic en "Create Zap"
2. Nombrar el Zap (ejemplo: "Copia de seguridad diaria de transacciones")

### Paso 3: configurar Trigger

#### Ejemplo: Schedule Trigger

```
App: Schedule by Zapier
Trigger Event: Every Day
Time of Day: 11:00pm (23:00)
Time Zone: Europe/Madrid
```

#### Ejemplo: Webhook Trigger

```
App: Webhooks by Zapier
Trigger Event: Catch Hook
```

Zapier proporcionará una URL como:
```
https://hooks.zapier.com/hooks/catch/123456/abcdef/
```

Esta URL se utilizará para recibir eventos de la API.

### Paso 4: configurar Actions

#### Action 1: GET Request a la API

```
App: Webhooks by Zapier
Action Event: GET
URL: https://tu-api.com/api/reports/daily
Headers:
  X-API-Key: api_key_demo_12345
```

**Test**: hacer clic en "Test & Continue" para verificar el funcionamiento.

#### Action 2: guardar en Google Sheets

```
App: Google Sheets
Action Event: Create Spreadsheet Row
Spreadsheet: [Seleccionar hoja de cálculo]
Worksheet: [Seleccionar pestaña]
```

Mapear campos:
- Fecha: `{{fecha}}`
- Monto: `{{monto_total}}`
- Transacciones: `{{num_transacciones}}`

## Características avanzadas

### Filtros y rutas

Los filtros permiten ejecutar acciones solo cuando se cumplen ciertas condiciones:

```
Filter by Zapier
Continue only if...
monto > 1000
AND
estado = completed
```

### Formateo de datos

Formatter by Zapier permite transformar datos:
- Formatear fechas
- Convertir divisas
- Manipular texto
- Operaciones matemáticas

### Code by Zapier

Para lógica personalizada, usar Python o JavaScript:

```python
# Ejemplo: calcular total y promedio
transacciones = input_data['transacciones']
total = sum(float(tx['monto']) for tx in transacciones)
promedio = total / len(transacciones)

output = {'total': total, 'promedio': promedio}
```

## Limitaciones

### Plan gratuito
- 100 tareas por mes
- Ejecución cada 15 minutos mínimo
- 5 Zaps activos

### Plan Starter (desde 19.99 USD/mes)
- 750 tareas por mes
- Multi-step Zaps
- Aplicaciones premium

## Seguridad

### Protección de API Key

No exponer la API Key directamente en URLs. Usar headers:

```
Headers:
  X-API-Key: {{api_key}}
```

### Validación de webhooks

Implementar firma HMAC para validar webhooks entrantes.

## Recursos adicionales

- [Documentación oficial de Zapier](https://zapier.com/help)
- [Zapier Community](https://community.zapier.com/)
- [API de referencia del sistema](../../README.md)


```
App: Google Sheets
Action Event: Create Spreadsheet Row
Drive: My Google Drive
Spreadsheet: Transacciones Backup
Worksheet: Reportes Diarios

Campos:
  - Fecha: (seleccionar campo 'fecha' del paso anterior)
  - Total Transacciones: (seleccionar 'total_transacciones')
  - Monto Total: (seleccionar 'monto_total')
  - Promedio: (seleccionar 'monto_promedio')
```

#### Action 3: Enviar Email

```
App: Email by Zapier
Action Event: Send Outbound Email
To: admin@tuempresa.com
Subject: Reporte Diario - {{fecha}}
Body:
  Resumen del día:
  
  Total transacciones: {{total_transacciones}}
  Monto total: ${{monto_total}}
  Promedio: ${{monto_promedio}}
  Máximo: ${{transaccion_maxima}}
  Mínimo: ${{transaccion_minima}}
  Clientes únicos: {{clientes_unicos}}
  
  Ver detalles en Google Sheets.
```

### Paso 5: Publicar Zap

1. Click "Publish"
2. Toggle ON
3. El Zap se ejecutará automáticamente

## Ejemplos detallados de Zaps

### Zap 1: Backup diario completo

**Objetivo**: Respaldar datos diarios en múltiples ubicaciones

#### Configuración paso a paso

**Step 1: Trigger**
```
App: Schedule by Zapier
Event: Every Day
Time: 11:00 PM
```

**Step 2: Get Report**
```
App: Webhooks by Zapier
Action: GET
URL: https://api.tuempresa.com/api/reports/daily
Headers: X-API-Key: tu_api_key
Query String Params: (vacío)
```

**Step 3: Format Date**
```
App: Formatter by Zapier
Event: Date / Time
Transform: Format
Input: {{Trigger date}}
To Format: YYYY-MM-DD
From Timezone: Europe/Madrid
To Timezone: Europe/Madrid
```

**Step 4: Google Sheets**
```
App: Google Sheets
Action: Create Spreadsheet Row
Spreadsheet: Backup Transacciones
Worksheet: Reportes
Row: 
  A: {{Step 3 output}}
  B: {{Step 2 total_transacciones}}
  C: {{Step 2 monto_total}}
  D: {{Step 2 monto_promedio}}
```

**Step 5: Dropbox**
```
App: Dropbox
Action: Upload File
Folder: /Backups/Transacciones
File Name: reporte_{{Step 3 output}}.json
File: {{Step 2 entire response}}
```

**Step 6: Slack**
```
App: Slack
Action: Send Channel Message
Channel: #finanzas
Message Text:
  :chart_with_upwards_trend: Reporte Diario Generado
  
  *Fecha:* {{Step 3 output}}
  *Transacciones:* {{Step 2 total_transacciones}}
  *Monto Total:* ${{Step 2 monto_total}}
```

### Zap 2: Alertas en tiempo real

**Objetivo**: Notificar transacciones grandes inmediatamente

#### Implementación con Webhook

**En tu API (opcional)** - Enviar webhook cuando hay transacción grande:

```python
# En routes.py, después de crear transacción
if transaction.monto > 1000:
    import requests
    webhook_url = "https://hooks.zapier.com/hooks/catch/123456/abcdef/"
    
    payload = {
        "id": transaction.id,
        "monto": float(transaction.monto),
        "moneda": transaction.moneda,
        "cliente": transaction.customer.nombre,
        "email": transaction.customer.email,
        "fecha": transaction.fecha.isoformat()
    }
    
    requests.post(webhook_url, json=payload)
```

**En Zapier**:

**Step 1: Trigger**
```
App: Webhooks by Zapier
Event: Catch Hook
(Copiar URL del webhook que Zapier proporciona)
```

**Step 2: Filter**
```
App: Filter by Zapier
Continue only if:
  monto (Number) Greater than 1000
```

**Step 3: Format**
```
App: Formatter by Zapier
Event: Numbers
Transform: Format Currency
Input: {{Step 1 monto}}
Currency: Euro
Decimals: 2
```

**Step 4: Send Email**
```
App: Email by Zapier
To: urgente@tuempresa.com
Subject: ALERTA - Transacción Grande - {{Step 3 output}}
Body:
  ALERTA: Transacción grande detectada
  
  Monto: {{Step 3 output}}
  Cliente: {{Step 1 cliente}}
  Email: {{Step 1 email}}
  ID: {{Step 1 id}}
  Fecha: {{Step 1 fecha}}
  
  Revisar inmediatamente.
```

**Step 5: Slack High Priority**
```
App: Slack
Action: Send Direct Message
User: @supervisor
Message:
  :rotating_light: *ALERTA: Transacción Grande*
  
  Monto: {{Step 3 output}}
  Cliente: {{Step 1 cliente}}
  ID: {{Step 1 id}}
```

**Step 6: Create Task**
```
App: Trello / Asana / Todoist
Action: Create Card/Task
Title: Revisar transacción #{{Step 1 id}} - {{Step 3 output}}
Description: Cliente: {{Step 1 cliente}}
Due Date: Today
Labels: urgent, high-value
```

### Zap 3: Multi-Path Zap (Paths)

**Objetivo**: Diferentes acciones según el monto de la transacción

**Step 1: Schedule** (cada hora)

**Step 2: GET Transactions**

**Step 3: Loop (si tienes plan profesional)** o usar Paths

**Path A: Transacciones grandes (>$1000)**
```
Filter: monto > 1000
→ Email urgente
→ Slack #ejecutivos
→ Create Jira ticket
```

**Path B: Transacciones medianas ($100-$1000)**
```
Filter: monto >= 100 AND monto <= 1000
→ Google Sheets log
→ Update dashboard
```

**Path C: Transacciones pequeñas (<$100)**
```
Filter: monto < 100
→ Solo log en Data Store
```

## Formatters útiles en Zapier

### Formatear números

```
App: Formatter by Zapier
Event: Numbers
Transform: Format Currency
Input: 1234.56
Currency: Euro
Output: €1,234.56
```

### Formatear texto

```
App: Formatter by Zapier
Event: Text
Transform: Titlecase
Input: {{customer_nombre}}
```

### Formatear fechas

```
App: Formatter by Zapier
Event: Date/Time
Transform: Format
Input: {{fecha}}
To Format: DD/MM/YYYY HH:mm
From Timezone: UTC
To Timezone: Europe/Madrid
```

### Calcular diferencias

```
App: Formatter by Zapier
Event: Numbers
Transform: Perform Math Operation
Input: {{monto_total}}
Operation: Subtract
Value: {{costos}}
```

## Código personalizado (Code by Zapier)

### Python Example

```python
# Available in Code by Zapier - Python

# Input data from previous steps
transaction_data = input_data.get('transactions', [])

# Process data
high_value = []
for tx in transaction_data:
    if float(tx['monto']) > 1000:
        high_value.append({
            'id': tx['id'],
            'monto': tx['monto'],
            'alert_level': 'HIGH'
        })

# Return output
output = {
    'high_value_count': len(high_value),
    'transactions': high_value
}
```

### JavaScript Example

```javascript
// Available in Code by Zapier - JavaScript

// Get input
const transactions = inputData.transactions;

// Process
const summary = {
  total: transactions.length,
  completed: 0,
  pending: 0,
  failed: 0
};

transactions.forEach(tx => {
  summary[tx.estado]++;
});

// Calculate percentage
summary.completion_rate = 
  (summary.completed / summary.total * 100).toFixed(2);

// Return
output = [summary];
```

## Filters avanzados

### Múltiples condiciones (AND)

```
Filter by Zapier
Continue only if ALL conditions are met:
  - monto (Number) Greater than 1000
  - moneda (Text) Exactly matches EUR
  - estado (Text) Exactly matches completed
```

### Múltiples condiciones (OR)

```
Filter by Zapier
Continue only if ANY condition is met:
  - tipo (Text) Exactly matches refund
  - estado (Text) Exactly matches failed
  - monto (Number) Greater than 5000
```

### Condiciones complejas

```
Filter by Zapier with Python Code
Code:
  monto = float(input_data['monto'])
  pais = input_data['pais']
  
  # Lógica personalizada
  is_suspicious = (monto > 1000 and pais != 'ES') or monto > 5000
  
  output = {'should_continue': is_suspicious}

Filter:
  should_continue (Boolean) Is True
```

## Storage (solo plan Teams+)

### Guardar valor

```
App: Storage by Zapier
Action: Set Value
Key: ultimo_reporte_fecha
Value: {{fecha}}
```

### Obtener valor

```
App: Storage by Zapier
Action: Get Value
Key: ultimo_reporte_fecha
Default Value: 2024-01-01
```

### Incrementar contador

```
App: Storage by Zapier
Action: Increment Value
Key: total_transacciones_procesadas
Increment By: 1
```

## Optimización de Tasks

### Estrategias para reducir consumo

1. **Usar filtros tempranos**: Filtra antes de acciones costosas
2. **Consolidar emails**: Un email con resumen vs múltiples emails
3. **Batch processing**: Procesar múltiples items a la vez
4. **Webhooks vs Polling**: Usar webhooks cuando sea posible

### Ejemplo de optimización

**Ineficiente** (30 tasks):
```
Trigger (0) → Get 10 transactions (1) → Loop 10 times (10) → 
Send email cada uno (10) → Update sheet cada uno (10) = 31 tasks
```

**Eficiente** (3 tasks):
```
Trigger (0) → Get transactions (1) → Format summary (1) → 
Send 1 email (1) = 3 tasks
```

## Solución de problemas

### Zap no se ejecuta

**Causa**: Zap desactivado o trigger mal configurado

**Solución**:
- Verifica que el toggle esté ON
- Comprueba el trigger (test step)
- Revisa el Task History para ver errores

### Error 401 en Webhook

**Causa**: API key incorrecta o no enviada

**Solución**:
- Verifica Headers en el paso de Webhook
- Asegura que `X-API-Key` esté presente
- Comprueba el valor de la key

### No llegan datos del step anterior

**Causa**: El step previo no devolvió datos

**Solución**:
- Haz test del step anterior
- Verifica que la respuesta tenga el formato esperado
- Usa Formatter para transformar si es necesario

### Límite de tasks superado

**Solución**:
- Revisa el Task History para identificar qué Zaps consumen más
- Optimiza Zaps según la sección anterior
- Considera actualizar tu plan

## Recursos adicionales

- [Zapier University](https://zapier.com/university)
- [Zapier Community](https://community.zapier.com/)
- [Zapier Help](https://help.zapier.com/)
- [Zapier Apps](https://zapier.com/apps)

## Plantillas útiles

### Template: Email alert

```
Sujeto: [ALERTA] Transacción {{tipo}} - ${{monto}}

Hola,

Se ha detectado una transacción que requiere atención:

Detalles:
- ID: {{id}}
- Monto: ${{monto}} {{moneda}}
- Cliente: {{customer_nombre}} ({{customer_email}})
- Tipo: {{tipo}}
- Estado: {{estado}}
- Fecha: {{fecha}}

Descripción: {{descripcion}}

Saludos,
Sistema Automatizado
```

### Template: Slack message

```markdown
:warning: *Nueva Transacción Detectada*

*Monto:* ${{monto}} {{moneda}}
*Cliente:* {{customer_nombre}}
*Estado:* {{estado}}
*Fecha:* {{fecha}}

<https://tu-dashboard.com/transactions/{{id}}|Ver detalles>
```

---

Para más ayuda, consulta la documentación del curso o abre un issue en el repositorio.
