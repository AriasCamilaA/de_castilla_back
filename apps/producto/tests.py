import requests
import pytest

def test_ver_productos_por_categoria():
    # Hacer la solicitud GET a la API para obtener todos los productos
    response = requests.get("https://de-castilla-back.onrender.com/castilla/api/productos/")
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    assert response.status_code == 200
    
    # Verificar que la respuesta contiene datos
    assert response.json() is not None
    
    # Seleccionar una categoría específica (en este caso, "Obleas")
    categoria_seleccionada = "Obleas"
    
    # Filtrar los productos por la categoría seleccionada
    productos_obleas = [producto for producto in response.json() if producto["categoria"]["nombre_categoria"] == categoria_seleccionada]
    
    # Verificar que se encuentren productos en la categoría seleccionada
    assert len(productos_obleas) > 0
    
    # Verificar que todos los productos pertenecen a la categoría seleccionada
    for producto in productos_obleas:
        assert producto["categoria"]["nombre_categoria"] == categoria_seleccionada