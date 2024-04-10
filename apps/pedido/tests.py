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
    # URL de la API
    url = "https://de-castilla-back.onrender.com/castilla/api/estadopedidos/"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    assert response.status_code == 200

    # Convertir la respuesta a formato JSON
    data = response.json()

    # Verificar que la respuesta no esté vacía
    assert data

    # Verificar que la lista de estados de pedido no esté vacía
    assert len(data) > 0

    # Verificar que cada estado de pedido tenga un ID y un nombre
    for estado_pedido in data:
        assert "id_estado_pedido" in estado_pedido
        assert "nombre_estado" in estado_pedido

    # Verificar que el estado de pedido "Por Aprobar" esté presente en la respuesta
    assert any(estado_pedido["nombre_estado"] == "Por Aprobar" for estado_pedido in data)

def test_visualizacion_detallada_pedido():
    # URL de la API
    url = "https://de-castilla-back.onrender.com/castilla/api/detallepedidos/70/"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    assert response.status_code == 200

    # Convertir la respuesta a formato JSON
    data = response.json()

    # Imprimir el detalle del pedido
    print("Detalle del Pedido:")
    print(data)

    # Verificar que la respuesta no esté vacía
    assert data

    # Verificar que la información detallada del pedido está presente en la respuesta
    assert "id_detalle_pedido" in data
    assert "producto" in data
    assert "pedido" in data
    assert "cantidad_producto" in data
    assert "subtotal_detalle_pedido" in data

    # Verificar que el estado del pedido esté presente en la respuesta
    assert "estado_pedido" in data["pedido"]
    assert "nombre_estado" in data["pedido"]["estado_pedido"]

    # Verificar que la información del usuario esté presente en la respuesta
    assert "usuario" in data["pedido"]
    assert "nombre_usuario" in data["pedido"]["usuario"]
    assert "apellido_usuario" in data["pedido"]["usuario"]
    assert "celular_usuario" in data["pedido"]["usuario"]
    assert "email" in data["pedido"]["usuario"]

    # Verificar que la información del producto esté presente en la respuesta
    assert "producto" in data
    assert "nombre_producto" in data["producto"]
    assert "imagen_producto" in data["producto"]
    assert "precio_producto" in data["producto"]

    # Verificar que el subtotal y la cantidad del producto sean valores válidos
    assert isinstance(data["cantidad_producto"], int) and data["cantidad_producto"] >= 0
    assert isinstance(data["subtotal_detalle_pedido"], int) and data["subtotal_detalle_pedido"] >= 0

def test_agregar_observaciones_al_crear_pedido():
    # Copia el diccionario original para no modificar los datos de prueba para otros tests
    pedido_con_observaciones = pedido_data_usuario.copy()

    observaciones = "Estas son algunas observaciones para el pedido"
    
    # Asigna las observaciones al campo correspondiente del diccionario
    pedido_con_observaciones["descripcion_pedido"] = observaciones

    # Realiza la petición POST para registrar un pedido con las observaciones
    response = requests.post(BASE_URL, json=pedido_con_observaciones)

    # Verificar que la solicitud se haya completado con éxito
    assert response.status_code == 201
    
    # Verificar que las observaciones se han agregado correctamente al pedido
    pedido_creado = response.json()
    assert pedido_creado["descripcion_pedido"] == observaciones

def test_calificar_pedido():
    # Datos del pedido a finalizar
    pedido_data = {
        "id_pedido": 21,
        "calificacion_pedido": 5
    }

    # Realizar la solicitud para finalizar el pedido y proporcionar una calificación
    response = requests.put(BASE_URL + str(pedido_data["id_pedido"]) + "/", json=pedido_data)

    # Verificar que la solicitud se haya realizado con éxito (código de estado 200)
    assert response.status_code == 200

    # Verificar que el sistema haya registrado la calificación del pedido correctamente
    pedido_actualizado = response.json()
    assert pedido_actualizado["calificacion_pedido"] == pedido_data["calificacion_pedido"]