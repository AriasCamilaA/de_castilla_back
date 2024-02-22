"""
URL configuration for de_castilla_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
   openapi.Info(
      title="Documentacio Castilla API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('castilla/api/', include('apps.calificacion.api.router')),
    path('castilla/api/', include('apps.categoria.api.router')),
    path('castilla/api/', include('apps.detalle_oc.api.router')),
    path('castilla/api/', include('apps.detalle_pedido.api.router')),
    path('castilla/api/', include('apps.detalle_venta.api.router')),
    path('castilla/api/', include('apps.estado_insumo.api.router')),
    path('castilla/api/', include('apps.estado_oc.api.router')),
    path('castilla/api/', include('apps.estado_pedido.api.router')),
    path('castilla/api/', include('apps.historico.api.router')),
    path('castilla/api/', include('apps.insumo.api.router')),
    path('castilla/api/', include('apps.inventario.api.router')),
    path('castilla/api/', include('apps.oc_has_provedor.api.router')),
    path('castilla/api/', include('apps.orden_compra.api.router')),
    path('castilla/api/', include('apps.pedido.api.router')),
    path('castilla/api/', include('apps.permiso.api.router')),
    path('castilla/api/', include('apps.producto.api.router')),
    path('castilla/api/', include('apps.proveedor.api.router')),
    path('castilla/api/', include('apps.rol.api.router')),
    path('castilla/api/', include('apps.rol_has_permisos.api.router')),
    path('castilla/api/', include('apps.sabor.api.router')),
    path('castilla/api/', include('apps.sabor_has_producto.api.router')),
    path('castilla/api/', include('apps.tipo_movimiento.api.router')),
    path('castilla/api/', include('apps.usuarios.api.router')),
    path('castilla/api/', include('apps.venta.api.router')),
    path('castilla/api/correo/', include('apps.correo.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
