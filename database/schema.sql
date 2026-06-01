-- ==============================================================================
-- Esquema de base de datos para sistema de gestión financiera
-- ==============================================================================
-- Compatible con: SQLite 3.x, PostgreSQL 12+
-- Versión: 1.0.0
-- Última actualización: 2026-06-01
-- ==============================================================================

-- ==============================================================================
-- Tabla: customers
-- Descripción: Almacena información de clientes del sistema
-- ==============================================================================
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    pais VARCHAR(50),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT 1 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Validaciones
    CONSTRAINT chk_email_format CHECK (email LIKE '%_@__%.__%'),
    CONSTRAINT chk_activo_bool CHECK (activo IN (0, 1))
);

-- Índices para tabla customers
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_pais ON customers(pais);
CREATE INDEX IF NOT EXISTS idx_customers_activo ON customers(activo);
CREATE INDEX IF NOT EXISTS idx_customers_nombre_apellido ON customers(nombre, apellido);

-- ==============================================================================
-- Tabla: transactions
-- Descripción: Registro de todas las transacciones financieras
-- ==============================================================================
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    
    -- Información monetaria
    monto DECIMAL(15, 4) NOT NULL,  -- Aumentado de 10,2 a 15,4 para mayor precisión
    moneda VARCHAR(3) DEFAULT 'USD' NOT NULL,
    
    -- Clasificación de transacción
    tipo VARCHAR(20) NOT NULL,  -- payment, refund, transfer, subscription, purchase
    estado VARCHAR(20) DEFAULT 'pending' NOT NULL,  -- pending, completed, failed, cancelled
    
    -- Información descriptiva
    descripcion VARCHAR(255),
    referencia_externa VARCHAR(100),
    
    -- Fechas
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_completado TIMESTAMP,
    
    -- Datos adicionales (formato JSON)
    extra_data TEXT,
    
    -- Auditoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Restricciones
    CONSTRAINT fk_transactions_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT chk_monto_positive CHECK (monto >= 0),
    CONSTRAINT chk_tipo_valid CHECK (tipo IN ('payment', 'refund', 'transfer', 'subscription', 'purchase')),
    CONSTRAINT chk_estado_valid CHECK (estado IN ('pending', 'completed', 'failed', 'cancelled')),
    CONSTRAINT chk_moneda_format CHECK (LENGTH(moneda) = 3)
);

-- Índices para tabla transactions
CREATE INDEX IF NOT EXISTS idx_transactions_customer_id ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_tipo ON transactions(tipo);
CREATE INDEX IF NOT EXISTS idx_transactions_estado ON transactions(estado);
CREATE INDEX IF NOT EXISTS idx_transactions_fecha ON transactions(fecha DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_moneda ON transactions(moneda);
CREATE INDEX IF NOT EXISTS idx_transactions_monto ON transactions(monto);
CREATE INDEX IF NOT EXISTS idx_transactions_referencia ON transactions(referencia_externa);

-- Índice compuesto para consultas comunes
CREATE INDEX IF NOT EXISTS idx_transactions_customer_fecha 
    ON transactions(customer_id, fecha DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_customer_estado 
    ON transactions(customer_id, estado);

-- ==============================================================================
-- Tabla: audit_logs
-- Descripción: Registro de auditoría para rastrear cambios en el sistema
-- ==============================================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER,
    
    -- Información de la acción
    accion VARCHAR(50) NOT NULL,  -- created, updated, deleted, status_changed
    usuario VARCHAR(100),
    ip_address VARCHAR(50),
    user_agent VARCHAR(255),
    
    -- Datos del cambio (formato JSON)
    datos_anteriores TEXT,
    datos_nuevos TEXT,
    
    -- Auditoría
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Restricciones
    CONSTRAINT fk_audit_transaction FOREIGN KEY (transaction_id) 
        REFERENCES transactions(id) ON DELETE SET NULL,
    CONSTRAINT chk_accion_valid CHECK (accion IN ('created', 'updated', 'deleted', 'status_changed'))
);

-- Índices para tabla audit_logs
CREATE INDEX IF NOT EXISTS idx_audit_transaction_id ON audit_logs(transaction_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_accion ON audit_logs(accion);
CREATE INDEX IF NOT EXISTS idx_audit_usuario ON audit_logs(usuario);

-- ==============================================================================
-- Tabla: stocks
-- Descripción: Información de acciones del mercado de valores
-- ==============================================================================
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Identificación
    simbolo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    
    -- Clasificación
    sector VARCHAR(100),
    mercado VARCHAR(50),
    moneda VARCHAR(3) DEFAULT 'USD' NOT NULL,
    
    -- Precios actuales
    precio_actual DECIMAL(15, 4),
    precio_apertura DECIMAL(15, 4),
    precio_cierre_anterior DECIMAL(15, 4),
    precio_max_dia DECIMAL(15, 4),
    precio_min_dia DECIMAL(15, 4),
    
    -- Cambios
    cambio_precio DECIMAL(15, 4),
    cambio_porcentaje DECIMAL(10, 4),
    
    -- Volumen
    volumen BIGINT,
    
    -- Metadatos
    activo BOOLEAN DEFAULT 1 NOT NULL,
    ultima_actualizacion TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Restricciones
    CONSTRAINT chk_simbolo_uppercase CHECK (simbolo = UPPER(simbolo)),
    CONSTRAINT chk_precios_positive CHECK (
        precio_actual >= 0 AND 
        precio_apertura >= 0 AND 
        precio_cierre_anterior >= 0
    ),
    CONSTRAINT chk_volumen_positive CHECK (volumen IS NULL OR volumen >= 0)
);

-- Índices para tabla stocks
CREATE INDEX IF NOT EXISTS idx_stocks_simbolo ON stocks(simbolo);
CREATE INDEX IF NOT EXISTS idx_stocks_sector ON stocks(sector);
CREATE INDEX IF NOT EXISTS idx_stocks_mercado ON stocks(mercado);
CREATE INDEX IF NOT EXISTS idx_stocks_activo ON stocks(activo);
CREATE INDEX IF NOT EXISTS idx_stocks_ultima_actualizacion ON stocks(ultima_actualizacion DESC);

-- ==============================================================================
-- Tabla: portfolios
-- Descripción: Posiciones de portafolio de clientes
-- ==============================================================================
CREATE TABLE IF NOT EXISTS portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    
    -- Cantidad de acciones
    cantidad DECIMAL(15, 4) NOT NULL,
    
    -- Precio de compra promedio
    precio_compra_promedio DECIMAL(15, 4) NOT NULL,
    
    -- Metadatos
    activo BOOLEAN DEFAULT 1 NOT NULL,
    fecha_primera_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Restricciones
    CONSTRAINT fk_portfolios_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT fk_portfolios_stock FOREIGN KEY (stock_id) 
        REFERENCES stocks(id) ON DELETE CASCADE,
    CONSTRAINT chk_cantidad_positive CHECK (cantidad > 0),
    CONSTRAINT chk_precio_compra_positive CHECK (precio_compra_promedio > 0),
    
    -- Un cliente no puede tener múltiples posiciones activas de la misma acción
    CONSTRAINT uq_customer_stock UNIQUE (customer_id, stock_id, activo)
);

-- Índices para tabla portfolios
CREATE INDEX IF NOT EXISTS idx_portfolios_customer_id ON portfolios(customer_id);
CREATE INDEX IF NOT EXISTS idx_portfolios_stock_id ON portfolios(stock_id);
CREATE INDEX IF NOT EXISTS idx_portfolios_activo ON portfolios(activo);

-- Índice compuesto para consultas de portafolio activo
CREATE INDEX IF NOT EXISTS idx_portfolios_customer_activo 
    ON portfolios(customer_id, activo);

-- ==============================================================================
-- Vistas útiles para consultas frecuentes
-- ==============================================================================

-- Vista: Resumen de clientes con su actividad
CREATE VIEW IF NOT EXISTS v_customer_summary AS
SELECT 
    c.id,
    c.email,
    c.nombre,
    c.apellido,
    c.pais,
    c.activo,
    COUNT(DISTINCT t.id) as total_transacciones,
    COALESCE(SUM(CASE WHEN t.estado = 'completed' THEN t.monto ELSE 0 END), 0) as monto_total_completado,
    COUNT(DISTINCT p.id) as total_posiciones_activas,
    c.created_at
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
LEFT JOIN portfolios p ON c.id = p.customer_id AND p.activo = 1
GROUP BY c.id;

-- Vista: Transacciones con información del cliente
CREATE VIEW IF NOT EXISTS v_transactions_detail AS
SELECT 
    t.id,
    t.customer_id,
    c.email as customer_email,
    c.nombre || ' ' || COALESCE(c.apellido, '') as customer_name,
    t.monto,
    t.moneda,
    t.tipo,
    t.estado,
    t.descripcion,
    t.referencia_externa,
    t.fecha,
    t.fecha_completado,
    t.created_at
FROM transactions t
INNER JOIN customers c ON t.customer_id = c.id;

-- Vista: Portafolios con valoración actual
CREATE VIEW IF NOT EXISTS v_portfolio_valuation AS
SELECT 
    p.id,
    p.customer_id,
    c.email as customer_email,
    c.nombre || ' ' || COALESCE(c.apellido, '') as customer_name,
    p.stock_id,
    s.simbolo as stock_symbol,
    s.nombre as stock_name,
    p.cantidad,
    p.precio_compra_promedio,
    s.precio_actual,
    (p.cantidad * p.precio_compra_promedio) as valor_compra,
    (p.cantidad * COALESCE(s.precio_actual, p.precio_compra_promedio)) as valor_actual,
    ((s.precio_actual - p.precio_compra_promedio) / p.precio_compra_promedio * 100) as rendimiento_porcentaje,
    p.fecha_primera_compra,
    p.activo
FROM portfolios p
INNER JOIN customers c ON p.customer_id = c.id
INNER JOIN stocks s ON p.stock_id = s.id;

-- ==============================================================================
-- Triggers para actualización automática de updated_at
-- ==============================================================================

-- Nota: Los triggers de SQLite para updated_at se implementan a continuación
-- Para PostgreSQL, se usaría una función y triggers diferentes

CREATE TRIGGER IF NOT EXISTS update_customers_timestamp 
AFTER UPDATE ON customers
BEGIN
    UPDATE customers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_transactions_timestamp 
AFTER UPDATE ON transactions
BEGIN
    UPDATE transactions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_stocks_timestamp 
AFTER UPDATE ON stocks
BEGIN
    UPDATE stocks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_portfolios_timestamp 
AFTER UPDATE ON portfolios
BEGIN
    UPDATE portfolios SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ==============================================================================
-- Fin del esquema de base de datos
-- ==============================================================================

