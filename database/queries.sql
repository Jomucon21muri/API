-- Consultas útiles para la base de datos financiera

-- ==================== CONSULTAS DE ANÁLISIS ====================

-- 1. Total de transacciones por cliente
SELECT 
    c.nombre,
    c.email,
    COUNT(t.id) as total_transacciones,
    SUM(t.monto) as gasto_total,
    AVG(t.monto) as gasto_promedio
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id
ORDER BY gasto_total DESC;

-- 2. Transacciones del último mes
SELECT 
    t.id,
    t.fecha,
    c.nombre,
    t.monto,
    t.moneda,
    t.tipo,
    t.estado
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.fecha >= datetime('now', '-30 days')
ORDER BY t.fecha DESC;

-- 3. Transacciones por estado
SELECT 
    estado,
    COUNT(*) as cantidad,
    SUM(monto) as monto_total
FROM transactions
GROUP BY estado;

-- 4. Top 10 transacciones más grandes
SELECT 
    t.id,
    c.nombre as cliente,
    t.monto,
    t.moneda,
    t.descripcion,
    t.fecha
FROM transactions t
JOIN customers c ON t.customer_id = c.id
ORDER BY t.monto DESC
LIMIT 10;

-- 5. Resumen diario de transacciones
SELECT 
    DATE(fecha) as dia,
    COUNT(*) as num_transacciones,
    SUM(monto) as total,
    AVG(monto) as promedio
FROM transactions
WHERE fecha >= datetime('now', '-30 days')
GROUP BY DATE(fecha)
ORDER BY dia DESC;

-- 6. Clientes con más transacciones
SELECT 
    c.nombre,
    c.email,
    COUNT(t.id) as num_transacciones
FROM customers c
JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id
ORDER BY num_transacciones DESC
LIMIT 10;

-- 7. Transacciones pendientes
SELECT 
    t.id,
    c.nombre as cliente,
    t.monto,
    t.moneda,
    t.descripcion,
    t.fecha
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.estado = 'pending'
ORDER BY t.fecha DESC;

-- 8. Devoluciones (refunds)
SELECT 
    t.id,
    c.nombre as cliente,
    t.monto,
    t.moneda,
    t.descripcion,
    t.fecha
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE t.tipo = 'refund'
ORDER BY t.fecha DESC;

-- 9. Transacciones por país
SELECT 
    c.pais,
    COUNT(t.id) as num_transacciones,
    SUM(t.monto) as total,
    AVG(t.monto) as promedio
FROM customers c
JOIN transactions t ON c.id = t.customer_id
GROUP BY c.pais
ORDER BY total DESC;

-- 10. Historial de auditoría reciente
SELECT 
    al.timestamp,
    al.accion,
    al.usuario,
    t.id as transaction_id,
    t.monto,
    c.nombre as cliente
FROM audit_logs al
JOIN transactions t ON al.transaction_id = t.id
JOIN customers c ON t.customer_id = c.id
ORDER BY al.timestamp DESC
LIMIT 20;

-- ==================== CONSULTAS DE REPORTES ====================

-- Reporte mensual completo
SELECT 
    strftime('%Y-%m', fecha) as mes,
    COUNT(*) as transacciones,
    SUM(CASE WHEN estado = 'completed' THEN monto ELSE 0 END) as ingresos,
    SUM(CASE WHEN tipo = 'refund' THEN monto ELSE 0 END) as devoluciones,
    COUNT(DISTINCT customer_id) as clientes_activos
FROM transactions
GROUP BY strftime('%Y-%m', fecha)
ORDER BY mes DESC;

-- Análisis de fraude potencial (múltiples transacciones en corto tiempo)
SELECT 
    customer_id,
    c.nombre,
    c.email,
    COUNT(*) as transacciones,
    SUM(monto) as total,
    MIN(fecha) as primera,
    MAX(fecha) as ultima
FROM transactions t
JOIN customers c ON t.customer_id = c.id
WHERE fecha >= datetime('now', '-1 hour')
GROUP BY customer_id
HAVING COUNT(*) > 3
ORDER BY transacciones DESC;

-- Clientes inactivos (sin transacciones recientes)
SELECT 
    c.id,
    c.nombre,
    c.email,
    MAX(t.fecha) as ultima_transaccion
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
WHERE c.activo = 1
GROUP BY c.id
HAVING MAX(t.fecha) < datetime('now', '-90 days') OR MAX(t.fecha) IS NULL
ORDER BY ultima_transaccion;

-- ==================== CONSULTAS DE MANTENIMIENTO ====================

-- Verificar integridad de datos
SELECT 'Clientes sin transacciones' as tipo, COUNT(*) as cantidad
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
WHERE t.id IS NULL

UNION ALL

SELECT 'Transacciones sin fecha_completado y estado completed', COUNT(*)
FROM transactions
WHERE estado = 'completed' AND fecha_completado IS NULL

UNION ALL

SELECT 'Transacciones con monto negativo', COUNT(*)
FROM transactions
WHERE monto < 0;

-- Limpieza: eliminar transacciones canceladas antiguas (>1 año)
-- DELETE FROM transactions 
-- WHERE estado = 'cancelled' 
-- AND fecha < datetime('now', '-365 days');

-- Actualizar updated_at de clientes activos
-- UPDATE customers 
-- SET updated_at = CURRENT_TIMESTAMP 
-- WHERE activo = 1;
