import requests
import pytest

# URL base de la API
BASE_URL = "https://de-castilla-back.onrender.com/castilla/api/pedidos/"

# Datos de ejemplo para el pedido
pedido_data_usuario = {
    "descripcion_pedido": "Sin descripción",
    "fecha_pedido": "2024-03-17",
    "fecha_fin_pedido": "2024-03-18",
    "calificacion_pedido": None,
    "estado": True,
    "id_estado_pedido_fk": 7,
    "no_Documento_Usuario_fk": 1234567890
}

def test_registrar_pedido():
    # Realizar la petición POST para registrar un pedido
    response = requests.post(BASE_URL, json=pedido_data_usuario)

    # Verificar si la petición fue exitosa (código de respuesta 201)
    if response.status_code == 201:

        assert "id_pedido" in response.json()
    elif response.status_code == 404:
    # Verificar si la respuesta contiene un mensaje de error indicando que el usuario no existe
        assert "error" in response.json() and "usuario no existe" in response.json()["error"]
    else:
    # Si la respuesta no es 201 ni 404, fallar el test
        assert False, f"Unexpected status code: {response.status_code}"

def test_mostrar_estado_pedido():
    # ID del pedido para el cual queremos verificar el estado
    id_pedido = 41

    # Realizar la petición GET para obtener el detalle del pedido
    response = requests.get(BASE_URL + str(id_pedido))

    # Verificar si la petición fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verificar si la respuesta contiene el estado actual del pedido
    pedido = response.json()
    assert "estado_pedido" in pedido
    assert "nombre_estado" in pedido["estado_pedido"]
    assert pedido["estado_pedido"]["nombre_estado"] == "Finalizados"

def test_actualizar_descripcion_pedido():
    # ID del pedido que queremos actualizar
    id_pedido = 39

    # Datos de ejemplo para actualizar la descripción del pedido
    pedido_data_actualizado = {
        "descripcion_pedido": "Nueva descripción del pedido",
        "fecha_pedido": "2024-03-17",
        "fecha_fin_pedido": "2024-03-18",
        "calificacion_pedido": None,
        "estado": True,
        "id_estado_pedido_fk": 7,
        "no_Documento_Usuario_fk": 1234567890
    }

    # Realizar la petición PUT para actualizar la descripción del pedido
    response = requests.put(BASE_URL + str(id_pedido), json=pedido_data_actualizado)

    # Verificar si la petición fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verificar si la descripción del pedido ha sido actualizada correctamente
    pedido_actualizado = response.json()
    assert pedido_actualizado["descripcion_pedido"] == pedido_data_actualizado["descripcion_pedido"]

if __name__ == "__main__":
    pytest.main([__file__])