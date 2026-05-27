"""
Script de prueba para la API Financiera
Ejecuta pruebas básicas contra la API
"""

import requests
import json
from datetime import datetime


# Configuración
BASE_URL = "http://localhost:5000/api"
API_KEY = "api_key_demo_12345"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def print_header(text):
    """Imprimir encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_result(test_name, success, data=None):
    """Imprimir resultado de prueba"""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status} - {test_name}")
    if data:
        print(f"     {data}")


def test_health():
    """Probar endpoint de salud"""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200
        print_result("Health endpoint", success, response.json().get('message'))
        return success
    except Exception as e:
        print_result("Health endpoint", False, str(e))
        return False


def test_authentication():
    """Probar autenticación"""
    print_header("TEST 2: Autenticación")
    
    # Sin API key
    try:
        response = requests.get(f"{BASE_URL}/customers")
        success = response.status_code == 401
        print_result("Sin API key → 401", success)
    except Exception as e:
        print_result("Sin API key", False, str(e))
        return False
    
    # Con API key correcta
    try:
        response = requests.get(f"{BASE_URL}/customers", headers=headers)
        success = response.status_code == 200
        print_result("Con API key → 200", success)
        return success
    except Exception as e:
        print_result("Con API key", False, str(e))
        return False


def test_get_customers():
    """Probar obtener clientes"""
    print_header("TEST 3: Listar Clientes")
    
    try:
        response = requests.get(f"{BASE_URL}/customers", headers=headers)
        data = response.json()
        
        success = response.status_code == 200 and 'data' in data
        num_clientes = len(data['data']) if success else 0
        
        print_result("GET /customers", success, f"{num_clientes} clientes encontrados")
        
        if success and num_clientes > 0:
            primer_cliente = data['data'][0]
            print(f"     Ejemplo: {primer_cliente['nombre']} ({primer_cliente['email']})")
        
        return success
    except Exception as e:
        print_result("GET /customers", False, str(e))
        return False


def test_get_transactions():
    """Probar obtener transacciones"""
    print_header("TEST 4: Listar Transacciones")
    
    try:
        response = requests.get(f"{BASE_URL}/transactions", headers=headers)
        data = response.json()
        
        success = response.status_code == 200 and 'data' in data
        num_transacciones = len(data['data']) if success else 0
        
        print_result("GET /transactions", success, f"{num_transacciones} transacciones encontradas")
        
        if success and num_transacciones > 0:
            primera = data['data'][0]
            print(f"     Ejemplo: ${primera['monto']} {primera['moneda']} - {primera['estado']}")
        
        return success
    except Exception as e:
        print_result("GET /transactions", False, str(e))
        return False


def test_create_transaction():
    """Probar crear transacción"""
    print_header("TEST 5: Crear Transacción")
    
    nueva_transaccion = {
        "customer_id": 1,
        "monto": 99.99,
        "moneda": "EUR",
        "tipo": "payment",
        "descripcion": "Test desde script de prueba"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/transactions",
            json=nueva_transaccion,
            headers=headers
        )
        data = response.json()
        
        success = response.status_code == 201 and data.get('success')
        
        print_result("POST /transactions", success)
        
        if success:
            print(f"     ID: {data['data']['id']}")
            print(f"     Monto: ${data['data']['monto']} {data['data']['moneda']}")
            return data['data']['id']
        
        return None
    except Exception as e:
        print_result("POST /transactions", False, str(e))
        return None


def test_update_transaction(transaction_id):
    """Probar actualizar transacción"""
    print_header("TEST 6: Actualizar Transacción")
    
    if not transaction_id:
        print_result("PATCH /transactions/{id}", False, "No hay ID de transacción")
        return False
    
    actualizacion = {
        "estado": "completed",
        "descripcion": "Actualizado desde script de prueba"
    }
    
    try:
        response = requests.patch(
            f"{BASE_URL}/transactions/{transaction_id}",
            json=actualizacion,
            headers=headers
        )
        data = response.json()
        
        success = response.status_code == 200 and data.get('success')
        print_result(f"PATCH /transactions/{transaction_id}", success)
        
        if success:
            print(f"     Nuevo estado: {data['data']['estado']}")
        
        return success
    except Exception as e:
        print_result("PATCH /transactions", False, str(e))
        return False


def test_filters():
    """Probar filtros de transacciones"""
    print_header("TEST 7: Filtros de Transacciones")
    
    # Filtro por estado
    try:
        response = requests.get(
            f"{BASE_URL}/transactions?estado=completed",
            headers=headers
        )
        data = response.json()
        success = response.status_code == 200
        print_result("Filtro por estado", success, f"{len(data['data'])} completadas")
    except Exception as e:
        print_result("Filtro por estado", False, str(e))
    
    # Filtro por monto mínimo
    try:
        response = requests.get(
            f"{BASE_URL}/transactions?monto_min=100",
            headers=headers
        )
        data = response.json()
        success = response.status_code == 200
        print_result("Filtro por monto", success, f"{len(data['data'])} > $100")
    except Exception as e:
        print_result("Filtro por monto", False, str(e))


def test_reports():
    """Probar reportes"""
    print_header("TEST 8: Reportes")
    
    # Reporte diario
    try:
        response = requests.get(f"{BASE_URL}/reports/daily", headers=headers)
        data = response.json()
        
        success = response.status_code == 200 and data.get('success')
        print_result("GET /reports/daily", success)
        
        if success:
            print(f"     Fecha: {data['fecha']}")
            print(f"     Transacciones: {data['total_transacciones']}")
            print(f"     Monto total: ${data['monto_total']}")
            print(f"     Promedio: ${data['monto_promedio']}")
    except Exception as e:
        print_result("GET /reports/daily", False, str(e))
    
    # Reporte de cliente
    try:
        response = requests.get(f"{BASE_URL}/reports/customer/1", headers=headers)
        data = response.json()
        
        success = response.status_code == 200 and data.get('success')
        print_result("GET /reports/customer/1", success)
        
        if success:
            print(f"     Cliente: {data['customer']['nombre']}")
            print(f"     Total transacciones: {data['total_transacciones']}")
            print(f"     Gasto total: ${data['gasto_total']}")
    except Exception as e:
        print_result("GET /reports/customer", False, str(e))


def test_exchange_rate():
    """Probar tipo de cambio"""
    print_header("TEST 9: Tipo de Cambio")
    
    monedas = ['USD', 'EUR', 'GBP', 'MXN']
    
    for moneda in monedas:
        try:
            response = requests.get(f"{BASE_URL}/exchange-rate/{moneda}", headers=headers)
            data = response.json()
            
            success = response.status_code == 200 and data.get('success')
            print_result(f"Tasa USD → {moneda}", success, f"Rate: {data.get('rate')}")
        except Exception as e:
            print_result(f"Tasa {moneda}", False, str(e))


def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("""
╔═══════════════════════════════════════════════╗
║  Script de Pruebas - API Financiera          ║
║  Ejecutando tests...                          ║
╚═══════════════════════════════════════════════╝
    """)
    
    # Verificar que la API está corriendo
    if not test_health():
        print("\n❌ Error: La API no está disponible.")
        print("   Asegúrate de que esté corriendo en http://localhost:5000")
        return
    
    # Ejecutar pruebas
    test_authentication()
    test_get_customers()
    test_get_transactions()
    
    transaction_id = test_create_transaction()
    test_update_transaction(transaction_id)
    
    test_filters()
    test_reports()
    test_exchange_rate()
    
    print("\n" + "="*60)
    print("  ✓ Todas las pruebas completadas")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_all_tests()
