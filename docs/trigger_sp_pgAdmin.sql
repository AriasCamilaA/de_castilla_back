/*__________________________________________________________

    TRIGGERS
__________________________________________________________*/





-- Crear venta asociada cuando el pedido finalice
CREATE OR REPLACE FUNCTION calcular_total_venta() RETURNS TRIGGER AS $$
DECLARE
    total_venta NUMERIC;
    fecha_fin DATE;
BEGIN
    IF NEW.id_estado_pedido_fk = 7 THEN -- 7 = Finalizado (estado pedido)
        -- Actualizar la fecha de finalización del pedido
        fecha_fin := CURRENT_DATE;

        -- Calcular el total de la venta sumando los subtotales de los detalles del pedido
        SELECT SUM(subtotal_detalle_pedido) INTO total_venta
        FROM detalle_pedido
        WHERE id_pedido_fk = NEW.id_pedido;

        -- Insertar en la tabla venta
        INSERT INTO venta (fecha_venta, hora_venta, total_venta, id_pedido_fk, no_documento_usuario_fk, estado)
        VALUES (CURRENT_DATE, CURRENT_TIME, total_venta, NEW.id_pedido, NEW.no_documento_usuario_fk, TRUE);

        -- Insertar detalles de la venta
        INSERT INTO detalle_venta (cantidad_producto, subtotal_detalle_venta, id_producto_fk, id_venta_fk, estado)
        SELECT cantidad_producto, subtotal_detalle_pedido, id_producto_fk, lastval(), TRUE
        FROM detalle_pedido
        WHERE id_pedido_fk = NEW.id_pedido;
    ELSIF NEW.id_estado_pedido_fk = 5 THEN
        -- Si el estado es Cancelado
        fecha_fin := CURRENT_DATE;
    ELSE 
        -- Si el estado no es 7 ni 5, mantener la fecha de finalización como NULL
        fecha_fin := NULL;
    END IF;

    -- Actualizar la fecha de finalización del pedido
    NEW.fecha_fin_pedido := fecha_fin;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_pedidofinalizado_BU
BEFORE UPDATE ON pedido
FOR EACH ROW
EXECUTE FUNCTION calcular_total_venta();


-- Registra la cantidad de insumos que entran cuando la orden de compra cambie de estado a finalizada
CREATE OR REPLACE FUNCTION registrar_historico_oc() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id_estado_oc_fk = 3 THEN
        -- Insertar en la tabla historico
        INSERT INTO historico (fecha_movimiento, cantidad_Historico, tipo_Historico, id_Insumo_FK, id_tipo_Movimiento_FK, estado)
        SELECT NOW(), detalle_oc.cantidad_insumo, 'INSUMO', detalle_oc.id_insumo_fk, 1, TRUE
        FROM detalle_oc
        WHERE detalle_oc.id_oc_fk = NEW.id_oc;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_ordencompra_finalizada_AU
AFTER UPDATE ON orden_compra
FOR EACH ROW
EXECUTE FUNCTION registrar_historico_oc();


-- Agregar registro a la tabla Inventario por cada insert en la tabla Insumo
CREATE OR REPLACE FUNCTION agregar_inventario_insumo() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO inventario (stock_inventario, id_insumo_fk, tipo_inventario, estado) VALUES (0, NEW.id_insumo, 'INSUMO', TRUE);
    INSERT INTO historico (fecha_movimiento, cantidad_historico, id_insumo_fk, id_tipo_movimiento_fk, tipo_historico, estado) 
    VALUES (NOW(), 0, NEW.id_insumo, 3, 'INSUMO', TRUE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_agregarInsumo_AI
AFTER INSERT ON insumo
FOR EACH ROW
EXECUTE FUNCTION agregar_inventario_insumo();


-- Agregar registro a la tabla Inventario por cada insert en la tabla Producto
CREATE OR REPLACE FUNCTION agregar_inventario_producto() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO inventario (stock_inventario, id_producto_fk, tipo_inventario, estado) VALUES (0, NEW.id_producto, 'PRODUCTO', TRUE);
    INSERT INTO historico (fecha_movimiento, cantidad_historico, id_producto_fk, id_tipo_movimiento_fk, tipo_historico, estado) 
    VALUES (NOW(), 0, NEW.id_producto, 3, 'PRODUCTO', TRUE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_agregarProducto_AI
AFTER INSERT ON producto 
FOR EACH ROW 
EXECUTE FUNCTION agregar_inventario_producto();


-- Actualizar la tabla Inventario por cada insert en la tabla Historico
CREATE OR REPLACE FUNCTION actualizar_inventario() RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.id_tipo_movimiento_fk = 1) THEN
        IF (NEW.tipo_historico = 'PRODUCTO') THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario + NEW.cantidad_historico 
            WHERE id_producto_fk = NEW.id_producto_fk;
        ELSEIF (NEW.tipo_historico = 'INSUMO') THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario + NEW.cantidad_historico 
            WHERE id_insumo_fk = NEW.id_insumo_fk;
        END IF;
    ELSEIF (NEW.id_tipo_movimiento_fk = 2) THEN
        IF (NEW.tipo_historico = 'PRODUCTO') THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario - NEW.cantidad_historico 
            WHERE id_producto_fk = NEW.id_producto_fk;
        ELSEIF (NEW.tipo_historico = 'INSUMO') THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario - NEW.cantidad_historico 
            WHERE id_insumo_fk = NEW.id_insumo_fk;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_SetStock_AI
AFTER INSERT ON historico
FOR EACH ROW
EXECUTE FUNCTION actualizar_inventario();


-- Agregar Calificación por defecto al proveedor cuando se crea uno nuevo
CREATE OR REPLACE FUNCTION calificar_proveedor() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO calificacion (estrellas_calificacion, id_proveedor_fk, comentario_Calificacion,estado)
    VALUES (5, NEW.id_proveedor,'Calificación por defecto',TRUE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_calificacionProveedor_AI
AFTER INSERT ON proveedor
FOR EACH ROW
EXECUTE FUNCTION calificar_proveedor();


-- Agregar historico cuando se agregue un detalle venta
CREATE OR REPLACE FUNCTION registrar_historico_detalle_venta() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO historico (cantidad_historico, fecha_movimiento, tipo_historico, id_producto_fk, id_tipo_movimiento_fk, estado)
    VALUES (NEW.cantidad_producto, NOW(), 'PRODUCTO', NEW.id_producto_fk, 2 ,TRUE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TG_registrarHistoricoDetalleVenta_AI
AFTER INSERT ON detalle_venta
FOR EACH ROW
EXECUTE FUNCTION registrar_historico_detalle_venta();



/*__________________________________________________________

    PROCEDIMIENTOS DE ALMACENADO
__________________________________________________________*/

-- Permite consultar cuáles son los productos (nombres) de una categoría. Si se pone solo '' mostrará los productos de todas las categorías.
CREATE OR REPLACE PROCEDURE SPobtenerProductosCategoria(miCategoria VARCHAR(255))
LANGUAGE plpgsql AS $$
BEGIN
    SELECT c.nombre_categoria AS CATEGORIA, p.nombre_producto AS PRODUCTO
    FROM categoria c
    LEFT JOIN producto p ON c.id_categoria = p.id_categoria_fk
    WHERE c.nombre_categoria LIKE '%' || miCategoria || '%' OR miCategoria = '';
END;
$$;

-- Permite consultar cuáles son los productos (nombres) de un sabor. Si se pone solo '' mostrará los productos de todos los sabores.
CREATE OR REPLACE PROCEDURE SPobtenerProductosSabor(miSabor VARCHAR(255))
LANGUAGE plpgsql AS $$
BEGIN
    SELECT s.nombre_sabor AS Sabor, p.nombre_producto AS PRODUCTO
    FROM sabor s
    LEFT JOIN sabor_has_producto sp ON s.id_sabor = sp.id_sabor_fk
    LEFT JOIN producto p ON sp.id_producto_fk = p.id_producto
    WHERE s.nombre_sabor LIKE '%' || miSabor || '%' OR miSabor = '';
END;
$$;

-- Permite consultar cuáles son los permisos y roles de un usuario buscando por número de documento, nombre, apellido. Si se pone solo '' mostrará los permisos y roles de todos los usuarios.
CREATE OR REPLACE PROCEDURE SProlesPermisosUsuario(datoUsuario VARCHAR(255))
LANGUAGE plpgsql AS $$
BEGIN
    SELECT u.no_documento_usuario AS DOCUMENTO, CONCAT(u.nombre_usuario, ' ', u.apellido_usuario) AS NOMBRE, r.nombre_rol AS ROL, p.descripcion_permiso AS PERMISO
    FROM usuario u
    LEFT JOIN rol r ON u.id_rol_fk = r.id_rol
    LEFT JOIN rol_has_permiso rp ON r.id_rol = rp.id_rol_fk
    LEFT JOIN permiso p ON rp.id_permiso_fk = p.id_permiso
    WHERE u.no_documento_usuario LIKE '%' || datoUsuario || '%'
        OR CONCAT(u.nombre_usuario, ' ', u.apellido_usuario) LIKE '%' || datoUsuario || '%'
        OR u.nombre_usuario LIKE '%' || datoUsuario || '%'
        OR u.apellido_usuario LIKE '%' || datoUsuario || '%'
        OR datoUsuario = '';
END;
$$;
