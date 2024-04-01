import pytest
import requests

@pytest.fixture
def api_url():
    return "http://de-castilla-back.onrender.com/castilla/api/login/"

def test_login(api_url):
    login_data = {
        "email": "Romero_Morales@example.com",
        "password": "1234ABCD*"
    }

    response = requests.post(api_url, json=login_data)

    assert response.status_code == 200

    assert "token" in response.json()


def test_password_reset():
    data = {
        "email": "Romero_Morales@example.com"
    }

    response = requests.post("http://de-castilla-back.onrender.com/castilla/api/password_reset/", json=data)

    assert response.status_code == 200

    json_response = response.json()
    assert "status" in json_response
    assert json_response["status"] == "OK"


def test_validacion_informacion_formulario():
    cliente_invalido = {
        "nombre_usuario": "UsuarioInvalido",
        "email": "correo_invalido"
    }

    response = requests.post("http://de-castilla-back.onrender.com/castilla/api/usuarios/", json=cliente_invalido)

    assert response.status_code == 400

    response_data = response.json()
    assert "email" in response_data
    assert "nombre_usuario" not in response_data
    assert "no_documento_usuario" in response_data


base_url = 'http://de-castilla-back.onrender.com/castilla/api/usuarios/'

def test_registro_cliente():
    nuevo_cliente = {
        "no_documento_usuario": 2138172,
        "password": "1234AD*21398+3",
        "apellido_usuario": "Rivas Palacios",
        "celular_usuario": 9012345682,
        "email": "asPalacios@example.com",
        "nombre_usuario": "Daniela Valentina",
        "estado": True,
        "is_active": True,
        "is_staff": True,
        "id_rol_fk": 2
    }

    response = requests.post(base_url, json=nuevo_cliente)

    if response.status_code != 201:
        print("Error al registrar el cliente:")
        print("Código de estado:", response.status_code)
        print("Contenido de la respuesta:", response.content.decode("utf-8"))
    
    assert response.status_code == 201