-- Datos de ejemplo para la base de datos

-- Insertar clientes de ejemplo
INSERT INTO customers (email, nombre, apellido, pais, telefono, activo) VALUES
('maria.garcia@email.com', 'María', 'García', 'ES', '+34600111222', 1),
('john.smith@email.com', 'John', 'Smith', 'US', '+1555123456', 1),
('pierre.dubois@email.com', 'Pierre', 'Dubois', 'FR', '+33612345678', 1),
('ana.martinez@email.com', 'Ana', 'Martínez', 'MX', '+525512345678', 1),
('carlos.rodriguez@email.com', 'Carlos', 'Rodríguez', 'ES', '+34600222333', 1),
('laura.fernandez@email.com', 'Laura', 'Fernández', 'ES', '+34600333444', 1),
('david.lopez@email.com', 'David', 'López', 'ES', '+34600444555', 1),
('elena.sanchez@email.com', 'Elena', 'Sánchez', 'ES', '+34600555666', 1),
('miguel.torres@email.com', 'Miguel', 'Torres', 'MX', '+525512346789', 1),
('sofia.ramirez@email.com', 'Sofía', 'Ramírez', 'MX', '+525512347890', 1);

-- Insertar transacciones de ejemplo
-- Transacciones de María García
INSERT INTO transactions (customer_id, monto, moneda, tipo, estado, descripcion, fecha) VALUES
(1, 150.00, 'EUR', 'payment', 'completed', 'Pago de suscripción mensual', datetime('now', '-5 days')),
(1, 75.50, 'EUR', 'payment', 'completed', 'Compra de productos', datetime('now', '-3 days')),
(1, 30.00, 'EUR', 'refund', 'completed', 'Devolución parcial', datetime('now', '-2 days')),

-- Transacciones de John Smith
(2, 500.00, 'USD', 'payment', 'completed', 'Consultoría profesional', datetime('now', '-7 days')),
(2, 1250.00, 'USD', 'payment', 'completed', 'Proyecto especial', datetime('now', '-4 days')),
(2, 85.00, 'USD', 'payment', 'pending', 'Servicio adicional', datetime('now', '-1 day')),

-- Transacciones de Pierre Dubois
(3, 200.00, 'EUR', 'payment', 'completed', 'Renovación anual', datetime('now', '-10 days')),
(3, 45.00, 'EUR', 'payment', 'completed', 'Compra adicional', datetime('now', '-6 days')),

-- Transacciones de Ana Martínez
(4, 3500.00, 'MXN', 'payment', 'completed', 'Pago grande', datetime('now', '-8 days')),
(4, 850.00, 'MXN', 'payment', 'completed', 'Servicio mensual', datetime('now', '-5 days')),
(4, 2100.00, 'MXN', 'payment', 'pending', 'Proyecto nuevo', datetime('now')),

-- Transacciones de Carlos Rodríguez
(5, 125.00, 'EUR', 'payment', 'completed', 'Suscripción premium', datetime('now', '-12 days')),
(5, 89.99, 'EUR', 'payment', 'completed', 'Compra online', datetime('now', '-9 days')),
(5, 45.00, 'EUR', 'payment', 'failed', 'Pago rechazado', datetime('now', '-3 days')),

-- Transacciones de Laura Fernández
(6, 250.00, 'EUR', 'payment', 'completed', 'Curso online', datetime('now', '-15 days')),
(6, 99.00, 'EUR', 'payment', 'completed', 'Material adicional', datetime('now', '-11 days')),

-- Transacciones de David López
(7, 1500.00, 'EUR', 'payment', 'completed', 'Servicio corporativo', datetime('now', '-20 days')),
(7, 350.00, 'EUR', 'payment', 'completed', 'Mantenimiento mensual', datetime('now', '-14 days')),
(7, 175.00, 'EUR', 'payment', 'completed', 'Actualización', datetime('now', '-7 days')),

-- Transacciones de Elena Sánchez
(8, 65.00, 'EUR', 'payment', 'completed', 'Suscripción básica', datetime('now', '-18 days')),
(8, 25.00, 'EUR', 'payment', 'completed', 'Extra mensual', datetime('now', '-13 days')),
(8, 40.00, 'EUR', 'payment', 'pending', 'Upgrade plan', datetime('now', '-2 days')),

-- Transacciones de Miguel Torres
(9, 4200.00, 'MXN', 'payment', 'completed', 'Pago trimestral', datetime('now', '-25 days')),
(9, 1100.00, 'MXN', 'payment', 'completed', 'Servicio adicional', datetime('now', '-16 days')),

-- Transacciones de Sofía Ramírez
(10, 750.00, 'MXN', 'payment', 'completed', 'Consultoría', datetime('now', '-22 days')),
(10, 380.00, 'MXN', 'payment', 'completed', 'Seguimiento mensual', datetime('now', '-10 days')),
(10, 520.00, 'MXN', 'payment', 'pending', 'Proyecto nuevo', datetime('now', '-1 day'));

-- Insertar registros de auditoría de ejemplo
INSERT INTO audit_logs (transaction_id, accion, usuario, ip_address, timestamp) VALUES
(1, 'created', 'system', '192.168.1.100', datetime('now', '-5 days')),
(1, 'updated', 'admin@sistema.com', '192.168.1.101', datetime('now', '-5 days', '+2 hours')),
(2, 'created', 'system', '192.168.1.100', datetime('now', '-3 days')),
(5, 'created', 'system', '192.168.1.100', datetime('now', '-4 days')),
(15, 'created', 'system', '192.168.1.100', datetime('now', '-3 days')),
(15, 'updated', 'admin@sistema.com', '192.168.1.102', datetime('now', '-3 days', '+1 hour'));
