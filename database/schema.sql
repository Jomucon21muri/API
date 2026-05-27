-- Esquema de base de datos para API Financiera
-- Compatible con SQLite y PostgreSQL

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    pais VARCHAR(50),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para customers
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_pais ON customers(pais);
CREATE INDEX IF NOT EXISTS idx_customers_activo ON customers(activo);

-- Tabla de transacciones
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    
    monto DECIMAL(10, 2) NOT NULL,
    moneda VARCHAR(3) DEFAULT 'USD',
    
    tipo VARCHAR(20) NOT NULL,  -- payment, refund, transfer
    estado VARCHAR(20) DEFAULT 'pending',  -- pending, completed, failed, cancelled
    
    descripcion VARCHAR(255),
    referencia_externa VARCHAR(100),
    
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_completado TIMESTAMP,
    
    metadata TEXT,  -- JSON
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Índices para transactions
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_tipo ON transactions(tipo);
CREATE INDEX IF NOT EXISTS idx_transactions_estado ON transactions(estado);
CREATE INDEX IF NOT EXISTS idx_transactions_fecha ON transactions(fecha);
CREATE INDEX IF NOT EXISTS idx_transactions_moneda ON transactions(moneda);
CREATE INDEX IF NOT EXISTS idx_transactions_monto ON transactions(monto);

-- Tabla de auditoría
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER,
    
    accion VARCHAR(50) NOT NULL,  -- created, updated, deleted
    usuario VARCHAR(100),
    ip_address VARCHAR(50),
    
    datos_anteriores TEXT,  -- JSON
    datos_nuevos TEXT,  -- JSON
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);

-- Índices para audit_logs
CREATE INDEX IF NOT EXISTS idx_audit_transaction ON audit_logs(transaction_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_accion ON audit_logs(accion);
