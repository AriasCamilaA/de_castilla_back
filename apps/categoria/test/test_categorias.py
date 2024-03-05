import django
import apps.categoria.models as Categoria
import pytest

django.setup()

class TestCategorias():

    @pytest.mark.django_db
    def test_categoria_crear(self):
        self.categoria = Categoria.Categoria.objects.create(
            descripcion_categoria = "Categoria de prueba",
            nombre_categoria = "Categoria de prueba",
            estado = True
        )
        assert self.categoria.nombre_categoria == 'Categoria de prueba'