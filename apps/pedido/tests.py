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

def test_cambiar_estado_pedido():
    # Datos de ejemplo para el cambio de estado del pedido
    cambio_estado_data = {
        "id_pedido": 1,
        "estado_pedido": {
            "id_estado_pedido": 3,
            "nombre_estado": "En Proceso",
            "estado": True
        },
        "usuario": {
            "no_documento_usuario": 7890123456,
            "rol": {
                "id_rol": 2,
                "nombre_rol": "Usuario",
                "estado": True
            },
            "password": "pbkdf2_sha256$720000$LwA8aP8OHOvRqWGnJKqzZZ$tNdX7A74LyzxiNO+4YSv3IAjsdBGEC3M3KwHJ7U0qgU=",
            "last_login": None,
            "is_superuser": True,
            "apellido_usuario": "Perez Torres",
            "celular_usuario": 7890123456,
            "email": "Perez_Torres@example.com",
            "nombre_usuario": "Valentina Alejandra",
            "estado": True,
            "is_active": True,
            "is_staff": True,
            "id_rol_fk": 2,
            "groups": [],
            "user_permissions": []
        },
        "descripcion_pedido": "Sin descripción",
        "fecha_pedido": "2023-06-12",
        "fecha_fin_pedido": "2024-03-17",
        "calificacion_pedido": None,
        "estado": True,
        "id_estado_pedido_fk": 5,
        "no_Documento_Usuario_fk": 7890123456
    }

    # Realizar la petición PUT para cambiar el estado del pedido
    response = requests.put(BASE_URL + "1/", json=cambio_estado_data)

    # Verificar si la petición fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verificar que el estado del pedido ha sido cambiado correctamente
    pedido_actualizado = response.json()
    assert pedido_actualizado["estado_pedido"]["nombre_estado"] == "Cancelado"

def test_obtener_pedido():
    response = requests.get(BASE_URL)
    print(response.json())  # Imprime la respuesta para ver su estructura
    assert response.status_code == 200  # Verificar que la solicitud sea exitosa
    pedidos = response.json()
    assert isinstance(pedidos, list)  # Verificar que la respuesta sea una lista

    # Asegúrate de que haya al menos un pedido en la lista
    assert len(pedidos) > 0

    # Tomamos el primer pedido de la lista
    primer_pedido = pedidos[0]
    assert isinstance(primer_pedido, dict)  # Verificar que el primer pedido sea un diccionario

    # Verificar que el pedido tenga las claves esperadas
    expected_keys = ["id_pedido", "estado_pedido", "usuario", "descripcion_pedido",
                     "fecha_pedido", "fecha_fin_pedido", "calificacion_pedido",
                     "estado", "id_estado_pedido_fk", "no_Documento_Usuario_fk"]
    for key in expected_keys:
        assert key in primer_pedido.keys()

    # Verificar que el estado del primer pedido sea "Finalizado"
    assert primer_pedido["estado_pedido"]["nombre_estado"] == "Finalizados"

    # Verificar que el usuario asociado al primer pedido tenga cierta información
    usuario = primer_pedido["usuario"]
    assert isinstance(usuario, dict)
    assert "nombre_usuario" in usuario.keys()
    assert "apellido_usuario" in usuario.keys()
    assert "email" in usuario.keys()