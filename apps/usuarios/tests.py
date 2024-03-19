import pytest
import requests

@pytest.fixture
def api_url():
    return "http://127.0.0.1:8000/castilla/api/login/"

def test_login(api_url):
    # Datos de ejemplo para el login
    login_data = {
        "email": "Ruiz_Jimenez@example.com",
        "password": "1234ABCD*"
    }

    # Realizar la solicitud POST para iniciar sesión
    response = requests.post(api_url, json=login_data)

    # Comprobar si la solicitud fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Comprobar si se recibió un token de autenticación en la respuesta
    assert "token" in response.json()

    # También puedes realizar otras afirmaciones sobre los datos de la respuesta si es necesario
