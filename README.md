# API castilla
## Pasos para configurar y ejecutar el backend:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/AriasCamilaA/de_castilla_back
   ```
   Moverse a la carpeta
   ```bash
   cd de_castilla_back
   ```
2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv env
   .\env\Scrips\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos MySQL:**

   (En MySQL)

   Eliminar la base de datos existente:

   ```bash
   DROP DATABASE IF EXISTS db_de_castilla;
   ```
   Crear la base de datos:
   ```bash
   CREATE DATABASE db_de_castilla;
   ```

5. **Aplicar migraciones:**
   
   (En la terminal dentro de la ubicación del proyecto y con el entorno activo)

   ```bash
   python manage.py migrate
   ```

6. **Ejecutar el script de triggers, storage proceudres y views:**

   Copiar el script _**db_views_triggers_SPs.sql**_ en la carpeta _**docs**_.

   Ejecutar el script en MySQL.

7. **Ejecutar el script de inserción de datos:**

   Copiar el script _**db_inserts.sql**_ en la carpeta _**docs**_.

   Ejecutar el script en MySQL.

8. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

## Rutas de acceso:

Para acceder a la documentación del API castilla: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

### Rutas actuales
- **Documentación**
   - docs/
   - redoc/
- **Calificaciones**
   - castilla/api/calificaciones/
   - castilla/api/calificaciones/<int:pk>/
   - calificaciones/generate-pdf
- **Categorias**
   - castilla/api/categorias/
   - castilla/api/categorias/<int:pk>/
   - categorias/generate-pdf/
- **Detalles Orden de Compra**
   - castilla/api/detalleocs/
   - castilla/api/detalleocs/<int:pk>/
   - detalleocs/generate-pdf/
- **Detalles de Pedidos**
   - castilla/api/detallepedidos/
   - castilla/api/detallepedidos/<int:pk>/
   - castilla/api/detallepedidos/pedido/<int:id_pedido_fk>/
   - castilla/api/detallepedidos/generate-pdf/<int:id_pedido>/
- **Detalles de Ventas**
   - castilla/api/detalleventas/
   - castilla/api/detalleventas/<int:pk>/
- **Estado de Insumos**
   - castilla/api/estadoinsumos/
   - castilla/api/estadoinsumos/<int:pk>/
   - estadoinsumo/generate-pdf/
- **Estado de Ordenes de Compra**
   - castilla/api/estadoocs/
   - castilla/api/estadoocs/<int:pk>/
   - estadoocs/generate-pdf
- **Estado de Pedidos**
   - castilla/api/estadopedidos/
   - castilla/api/estadopedidos/<int:pk>/
   - estadopedidos/generate-pdf/
- **Historicos**
   - castilla/api/historicos/
   - castilla/api/historicos/<int:pk>/
   - historicos/generate-pdf/
- **Insumos**
   - castilla/api/insumos/
   - castilla/api/insumos/<int:pk>/
- **Inventarios**
   - castilla/api/inventario/
   - castilla/api/inventario/<int:pk>/
- **Ordenes de Compra has Provedores**
   - castilla/api/ochasproveedores/
   - castilla/api/ochasproveedores/<int:pk>/
- **Ordenes de Compra**
   - castilla/api/ordencompras/
   - castilla/api/ordencompras/<int:pk>/
- **Pedidos**
   - castilla/api/pedidos/
   - castilla/api/pedidos/<int:pk>/
   - castilla/api/pedidos/generate-pdf/ 
- **Permisos**
   - castilla/api/permisos/
   - castilla/api/permisos/<int:pk>/
- **Productos**
   - castilla/api/productos/
   - castilla/api/productos/<int:pk>/
- **Proveedores**
   - castilla/api/proveedores/
   - castilla/api/proveedores/<int:pk>/
- **Roles**
   - castilla/api/roles/
   - castilla/api/roles/<int:pk>/
- **Roles has Permisos**
   - castilla/api/rolHaspermisos/
   - castilla/api/rolHaspermisos/<int:pk>/
- **Sabores**
   - castilla/api/sabores/
   - castilla/api/sabores/<int:pk>/
- **Sabores has Productos**
   - castilla/api/saborhasproductos/
   - castilla/api/saborhasproductos/<int:pk>/
- **Tipo de movimientos**
   - castilla/api/timpomovientos/
   - castilla/api/timpomovientos/<int:pk>/
- **Usuarios**
   - castilla/api/usuarios/
   - castilla/api/usuarios/<int:pk>/
- **Login**
   - castilla/api/login/ 
   - castilla/api/login/refresh/ 
- **Ventas**
   - castilla/api/ventas/
   - castilla/api/ventas/<int:pk>/



