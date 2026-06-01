# Integración Make con sistema de gestión financiera

Este directorio contiene escenarios de ejemplo para Make (anteriormente Integromat) que se integran con la API del sistema de gestión financiera.

## Escenarios disponibles

### 1. Sincronización con Google Sheets

**Descripción**: sincroniza transacciones con Google Sheets cada hora.

**Módulos utilizados**:
- Schedule (cada hora)
- HTTP - Make a request (GET transacciones)
- Iterator (procesar cada transacción)
- Google Sheets - Add a row
- Data store (evitar duplicados)

### 2. Sistema de alertas multicanal

**Descripción**: monitorea transacciones grandes y envía alertas por múltiples canales.

**Flujo**:
1. Webhook trigger o Schedule
2. HTTP Request (GET transacciones)
3. Router (dividir por criterios)
4. Filtros (monto, país, tipo)
5. Notificaciones (correo electrónico, Slack, SMS)

### 3. Detección de fraude

**Descripción**: detecta patrones sospechosos y crea alertas.

**Criterios de detección**:
- Múltiples transacciones en poco tiempo
- Transacciones desde países diferentes
- Montos inusuales
- Patrones de velocidad anormales

## Instalación y configuración

### Paso 1: crear cuenta en Make

1. Visitar [make.com](https://www.make.com)
2. Registrar una cuenta (plan gratuito disponible)
3. Verificar dirección de correo electrónico

### Paso 2: importar escenario

1. En Make, hacer clic en "Create a new scenario"
2. Hacer clic en los tres puntos (⋯) → "Import Blueprint"
3. Seleccionar el archivo JSON
4. Hacer clic en "Save"

### Paso 3: configurar conexiones

#### HTTP Request - API financiera

En cada módulo HTTP:

1. **URL**: `http://tu-api.com/api/transactions`
   - Para pruebas locales con ngrok: `https://xxxx.ngrok.io/api/transactions`

2. **Method**: GET (o POST según el caso)

3. **Headers**:
   - Hacer clic en "Add item"
   - Name: `X-API-Key`
   - Value: `api_key_demo_12345`

4. **Parse response**: YES

#### Google Sheets

1. Hacer clic en "Create a connection"
2. Autorizar cuenta de Google
3. Seleccionar el Spreadsheet
4. Seleccionar la hoja (Sheet)

### Paso 4: configurar Data Store (opcional)

Para evitar duplicados:

1. En Make, ir a "Data stores"
2. Hacer clic en "Add data store"
3. Nombre: "Transacciones procesadas"
4. Data structure:
   ```json
   {
     "transaction_id": "",
     "fecha_procesado": ""
   }
   ```

### Paso 5: activar escenario

1. Hacer clic en "Scheduling" (reloj) en la esquina inferior izquierda
2. Activar el escenario

## Características avanzadas

### Variables de entorno

Se recomienda utilizar variables de Make para almacenar:
- URL de la API
- API Key
- Configuraciones de umbral

### Manejo de errores

Configurar manejadores de errores en módulos críticos:
1. Hacer clic derecho en el módulo
2. Seleccionar "Add error handler"
3. Configurar acción de fallback

### Limitaciones del plan gratuito

- 1000 operaciones por mes
- Ejecución cada 15 minutos mínimo
- 2 escenarios activos simultáneos

## Recursos adicionales

- [Documentación oficial de Make](https://www.make.com/en/help)
- [Comunidad Make](https://community.make.com/)
- [API de referencia del sistema](../../README.md)

3. Configura frecuencia de ejecución

## Ejemplo de escenario paso a paso

### Escenario: Sincronización con Google Sheets

#### Módulo 1: Schedule

```
Interval: 1 hour
Starting: Immediately
```

#### Módulo 2: HTTP Request

```
URL: http://tu-api.com/api/transactions
Method: GET
Headers:
  - X-API-Key: api_key_demo_12345
Parse response: Yes
```

#### Módulo 3: Filter - Solo nuevas

```
Label: Solo últimas 24 horas
Condition:
  fecha (Date) is greater than {{now - 1 day}}
```

#### Módulo 4: Iterator

```
Array: {{2.data}}
```

Este módulo itera sobre cada transacción

#### Módulo 5: Data Store - Search

```
Data Store: Transacciones procesadas
Key: {{4.id}}
```

#### Módulo 6: Filter - No procesada

```
Label: Solo no procesadas
Condition:
  {{5.id}} Does not exist
```

#### Módulo 7: Google Sheets - Add a row

```
Spreadsheet: Tu spreadsheet
Sheet: Transacciones
Values:
  - ID: {{4.id}}
  - Fecha: {{4.fecha}}
  - Cliente: {{4.customer_nombre}}
  - Email: {{4.customer_email}}
  - Monto: {{4.monto}}
  - Moneda: {{4.moneda}}
  - Tipo: {{4.tipo}}
  - Estado: {{4.estado}}
  - Descripción: {{4.descripcion}}
```

#### Módulo 8: Data Store - Add record

```
Data Store: Transacciones procesadas
Key: {{4.id}}
Data:
  transaction_id: {{4.id}}
  fecha_procesado: {{now}}
```

## Router avanzado para alertas

### Configuración de Router

```
Router
├── Route 1: Transacciones grandes (>$1000)
│   ├── Filter: monto > 1000
│   ├── Email - Alta prioridad
│   └── Slack - Canal #finanzas
│
├── Route 2: Transacciones internacionales
│   ├── Filter: pais != ES
│   ├── Email - Equipo internacional
│   └── Log to Data store
│
└── Route 3: Transacciones fallidas
    ├── Filter: estado = failed
    ├── Email - Soporte técnico
    └── Create Jira ticket
```

### Ejemplo de Filter

**Transacciones grandes**:
```
Label: Monto mayor a 1000
Condition: {{monto}} Numeric operator: Greater than 1000
```

**País específico**:
```
Label: Solo España
Condition: {{customer.pais}} Text operator: Equal to ES
```

**Múltiples condiciones (AND)**:
```
Label: Grandes y completadas
Conditions:
  {{monto}} > 1000
  AND
  {{estado}} = completed
```

**Múltiples condiciones (OR)**:
```
Label: USD o EUR
Conditions:
  {{moneda}} = USD
  OR
  {{moneda}} = EUR
```

## Funciones útiles en Make

### Formatear fecha

```
{{formatDate(fecha; "DD/MM/YYYY HH:mm")}}
```

### Redondear números

```
{{round(monto; 2)}}
```

### Condicional

```
{{if(monto > 1000; "Grande"; "Normal")}}
```

### Concatenar texto

```
{{cliente}} - ${{monto}} {{moneda}}
```

### Obtener fecha actual

```
{{now}}
{{addDays(now; -7)}}  // Hace 7 días
{{formatDate(now; "YYYY-MM-DD")}}
```

## Ejemplos de notificaciones

### Email con formato

```
Module: Email - Send an email
To: admin@tuempresa.com
Subject: Transacción grande detectada - ${{monto}}
Content Type: HTML
Content:
  <h2>Alerta de Transacción</h2>
  <p><strong>ID:</strong> {{id}}</p>
  <p><strong>Monto:</strong> ${{monto}} {{moneda}}</p>
  <p><strong>Cliente:</strong> {{customer_nombre}}</p>
  <p><strong>Email:</strong> {{customer_email}}</p>
  <p><strong>Fecha:</strong> {{formatDate(fecha; "DD/MM/YYYY HH:mm")}}</p>
  <p><strong>Estado:</strong> {{estado}}</p>
```

### Slack

```
Module: Slack - Create a message
Channel: #finanzas
Text:
  :warning: *Transacción Grande Detectada*
  
  *Monto:* ${{monto}} {{moneda}}
  *Cliente:* {{customer_nombre}} ({{customer_email}})
  *Fecha:* {{formatDate(fecha; "DD/MM/YYYY HH:mm")}}
  *Estado:* {{estado}}
  *Descripción:* {{descripcion}}
```

### SMS (Twilio)

```
Module: Twilio - Send SMS
To: +34600111222
Body: Alerta: Transacción de ${{monto}} {{moneda}} de {{customer_nombre}}. ID: {{id}}
```

## Optimización de operaciones

### Tips para reducir consumo

1. **Usar filtros tempranos**: Filtra antes de iterar
2. **Batch processing**: Agrupa múltiples registros
3. **Data stores**: Evita procesar duplicados
4. **Webhooks**: Usa triggers de eventos en vez de polling

### Ejemplo de optimización

**Ineficiente** (100 operaciones):
```
Schedule → HTTP Request → Iterator (100 items) → Google Sheets
= 1 + 1 + 100 = 102 operaciones
```

**Eficiente** (2 operaciones):
```
Schedule → HTTP Request → Google Sheets (bulk insert)
= 1 + 1 = 2 operaciones
```

## Solución de problemas

### Error: "Invalid JSON"

**Causa**: La API no devuelve JSON válido

**Solución**:
- Verifica la URL de la API
- Comprueba que el endpoint devuelve JSON
- Agrega header `Accept: application/json`

### Error: "401 Unauthorized"

**Causa**: API key incorrecta

**Solución**:
- Verifica el header `X-API-Key`
- Comprueba el valor de la API key

### Escenario no se ejecuta

**Causa**: Scheduling desactivado

**Solución**:
- Activa el Scheduling (toggle en esquina inferior)
- Verifica que el trigger esté configurado

### Too many operations

**Causa**: Superaste el límite de operaciones

**Solución**:
- Optimiza el escenario (ver sección de optimización)
- Actualiza tu plan de Make
- Reduce la frecuencia de ejecución

## Recursos adicionales

- [Make Academy](https://www.make.com/en/academy)
- [Make Community](https://community.make.com/)
- [Documentación Make](https://www.make.com/en/help)
- [Templates Make](https://www.make.com/en/templates)
