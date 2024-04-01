import requests
import pytest

BASE_URL = "https://de-castilla-back.onrender.com/castilla/api/"

ejemplo_venta = {
    "fecha_venta": "2024-03-31",
    "hora_venta": "12:00",
    "total_venta": 10000,
    "estado": True,
    "id_cliente": 1,
    "nombre_cliente": "Camila Alexandra",
    "id_pedido_fk": None,
    "no_documento_usuario_fk": 1234567890
}

ejemplo_detalle_venta = {
    "cantidad_producto": 2,
    "subtotal_detalle_venta": 5000,
    "estado": True,
    "id_producto_fk": 1,
    "id_venta_fk": 1
}

@pytest.mark.parametrize("venta_data", [ejemplo_venta])
def test_registro_venta(venta_data):
    # Hacer la solicitud POST para registrar la venta
    response_venta = requests.post(BASE_URL + "ventas/", json=venta_data)
    assert response_venta.status_code == 201 

    id_venta = response_venta.json().get("id")

    ejemplo_detalle_venta["id_venta_fk"] = id_venta

    response_detalle_venta = requests.post(BASE_URL + "detalleventas/", json=ejemplo_detalle_venta)
    assert response_detalle_venta.status_code == 201