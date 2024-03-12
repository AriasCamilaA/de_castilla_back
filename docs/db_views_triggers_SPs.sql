/*__________________________________________________________

    TRIGGERS
__________________________________________________________*/
use db_de_castilla;


/*---Crear venta asociada cuando el pedido finalice ---*/
DELIMITER $$

CREATE TRIGGER TG_pedidofinalizado_AU AFTER UPDATE ON pedido
FOR EACH ROW
BEGIN
    DECLARE total_venta BIGINT;
    IF NEW.id_estado_pedido_fk = 7 THEN -- 7 = Finalizado (estado pedido)
        -- Calcular el total de la venta sumando los subtotales de los detalles del pedido
        SELECT SUM(subtotal_detalle_pedido) INTO total_venta
        FROM detalle_pedido
        WHERE id_pedido_fk = NEW.id_pedido;

        -- Insertar en la tabla venta
        INSERT INTO venta (fecha_venta, hora_venta, total_venta, id_pedido_fk, no_documento_usuario_fk, estado)
        VALUES (CURDATE(), CURTIME(), total_venta, NEW.id_pedido, NEW.no_documento_usuario_fk, 1);

        -- Obtener el id de la venta recién insertada
        SET @id_venta = LAST_INSERT_ID();

        -- Insertar detalles de la venta
        INSERT INTO detalle_venta (cantidad_producto, subtotal_detalle_venta, id_producto_fk, id_venta_fk, estado)
        SELECT cantidad_producto, subtotal_detalle_pedido, id_producto_fk, @id_venta, 1
        FROM detalle_pedido
        WHERE id_pedido_fk = NEW.id_pedido;
    END IF;
END$$

DELIMITER ;



/*---Agregar registro a la tabla Inventario por cada insert en la tabla Insumo ---*/
DELIMITER $$
CREATE TRIGGER TG_agregarInsumo_AI AFTER INSERT ON insumo
FOR EACH ROW
BEGIN
    INSERT INTO inventario (stock_inventario, id_insumo_fk, tipo_inventario, estado) VALUES (0, NEW.id_insumo, "INSUMO",1);
    INSERT INTO historico (fecha_movimiento, cantidad_historico, id_insumo_fk, id_tipo_movimiento_fk, tipo_historico, estado) 
    VALUES (NOW(), 0, NEW.id_insumo, 2, "INSUMO", 1);
END$$
DELIMITER ;

/*---Agregar registro a la tabla Inventario por cada insert en la tabla Producto ---*/
DELIMITER $$
CREATE TRIGGER TG_agregarProducto_AI AFTER INSERT ON producto 
FOR EACH ROW 
BEGIN
    INSERT INTO inventario (stock_inventario, id_producto_fk, tipo_inventario, estado) VALUES (0, NEW.id_producto, "PRODUCTO", 1);
    INSERT INTO historico (fecha_movimiento, cantidad_historico, id_producto_fk, id_tipo_movimiento_fk, tipo_historico, estado) 
    VALUES (NOW(), 0, NEW.id_producto, 2, "PRODUCTO",1);
END$$
DELIMITER ;

/*---Actualizar la tabla Inventario por cada insert en la tabla Historico ---*/
DELIMITER $$
CREATE TRIGGER TG_SetStock_AI AFTER INSERT ON historico
FOR EACH ROW
BEGIN
    IF (NEW.id_tipo_movimiento_fk = 1) THEN
        IF (NEW.tipo_historico = "PRODUCTO") THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario + NEW.cantidad_historico 
            WHERE id_producto_fk = NEW.id_producto_fk;
        ELSEIF (NEW.tipo_historico = "INSUMO") THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario + NEW.cantidad_historico 
            WHERE id_insumo_fk = NEW.id_insumo_fk;
        END IF;
    ELSEIF (NEW.id_tipo_movimiento_fk = 2) THEN
        IF (NEW.tipo_historico = "PRODUCTO") THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario - NEW.cantidad_historico 
            WHERE id_producto_fk = NEW.id_producto_fk;
        ELSEIF (NEW.tipo_historico = "INSUMO") THEN
            UPDATE inventario SET 
                stock_inventario = stock_inventario - NEW.cantidad_historico 
            WHERE id_insumo_fk = NEW.id_insumo_fk;
        END IF;
    END IF;
END$$



/*---Agregar Calificación por defecto al proveedor cuando se crea uno nuevo --*/
DELIMITER $$
CREATE TRIGGER TG_calificacionProveedor_AI AFTER INSERT ON proveedor
FOR EACH ROW
BEGIN
    INSERT INTO calificacion (estrellas_calificacion, id_proveedor_fk, comentario_Calificacion,estado) -- Cambié estrallas_calificacion a estrellas_calificacion
    VALUES (5, NEW.id_proveedor,'Calificación por defecto',1);
END$$

DELIMITER ;

/*---Agregar historico cuando se agregue un detalle venta---*/
DELIMITER $$

CREATE TRIGGER TG_registrarHistoricoDetalleVenta_AI AFTER INSERT ON detalle_venta
FOR EACH ROW
BEGIN
    DECLARE producto_id INT;
    DECLARE cantidad_venta INT;

    -- Obtener el id del producto y la cantidad vendida
    SELECT NEW.id_producto_fk INTO producto_id;
    SELECT NEW.cantidad_producto INTO cantidad_venta;
    -- FROM detalle_venta
    -- WHERE id_detalle_venta = NEW.id_detalle_venta;



    -- Insertar en el historico
    INSERT INTO historico (cantidad_historico, fecha_movimiento, tipo_historico, id_producto_fk, id_tipo_movimiento_fk, estado)
    VALUES (cantidad_venta, NOW(), 'PRODUCTO', producto_id, 2 ,1);
END$$

DELIMITER ;


/*__________________________________________________________

    PROCEDIMIENTOS DE ALMACENADO
__________________________________________________________*/

/*-- Permite consultar cuáles son los productos (nombres) de una categoría. Si se pone solo '' mostrará los productos de todas las categorías. --*/
DELIMITER $$
CREATE PROCEDURE SPobtenerProductosCategoria(IN miCategoria VARCHAR(255))
BEGIN
	SELECT c.nombre_categoria AS CATEGORIA, p.nombre_producto AS PRODUCTO
	FROM categoria c
	LEFT JOIN producto p ON c.id_categoria = p.id_categoria_fk
	WHERE c.nombre_categoria LIKE CONCAT('%', miCategoria, '%') OR miCategoria = '';
END$$
DELIMITER ;

/*-- Permite consultar cuáles son los productos (nombres) de un sabor. Si se pone solo '' mostrará los productos de todos los sabores. --*/
DELIMITER $$
CREATE PROCEDURE SPobtenerProductosSabor(IN miSabor VARCHAR(255))
BEGIN
	SELECT s.nombre_sabor AS Sabor, p.nombre_producto AS PRODUCTO
	FROM sabor s
	LEFT JOIN sabor_has_producto sp ON s.id_sabor = sp.id_sabor_fk
	LEFT JOIN producto p ON sp.id_producto_fk = p.id_producto
	WHERE s.nombre_sabor LIKE CONCAT('%', miSabor, '%') OR miSabor = '';
END$$
DELIMITER ;

/*-- Permite consultar cuáles son los permisos y roles de un usuario buscando por número de documento, nombre, apellido. Si se pone solo '' mostrará los permisos y roles de todos los usuarios. --*/
DELIMITER $$
CREATE PROCEDURE SProlesPermisosUsuario(IN datoUsuario VARCHAR(255))
BEGIN
	SELECT u.no_documento_usuario AS DOCUMENTO, CONCAT(u.nombre_usuario, ' ', u.apellido_usuario) AS NOMBRE, r.nombre_rol AS ROL, p.descripcion_permiso AS PERMISO
	FROM usuario u
	LEFT JOIN rol r ON u.id_rol_fk = r.id_rol
	LEFT JOIN rol_has_permiso rp ON r.id_rol = rp.id_rol_fk
	LEFT JOIN permiso p ON rp.id_permiso_fk = p.id_permiso
	WHERE u.no_documento_usuario LIKE CONCAT('%', datoUsuario, '%')
		OR CONCAT(u.nombre_usuario, ' ', u.apellido_usuario) LIKE CONCAT('%', datoUsuario, '%')
		OR u.nombre_usuario LIKE CONCAT('%', datoUsuario, '%')
		OR u.apellido_usuario LIKE CONCAT('%', datoUsuario, '%')
		OR datoUsuario = '';
END$$
DELIMITER ;

/*__________________________________________________________

    VISTAS
__________________________________________________________*/

/*-----------Inventario de insumo-----------*/
CREATE VIEW VW_INVENTARIO_INSUMO AS
SELECT Inventario.id_insumo_fk AS ID,
    Insumo.nombre_insumo AS INSUMO,
    SUM(IF(Historico.id_tipo_movimiento_fk = 1, Historico.cantidad_historico, 0)) AS ENTRADAS,
    SUM(IF(Historico.id_tipo_movimiento_fk = 2, Historico.cantidad_historico, 0)) AS SALIDAS,
    Inventario.stock_inventario AS STOCK
FROM Inventario
INNER JOIN Insumo ON Inventario.id_insumo_fk = Insumo.id_insumo
INNER JOIN Historico ON Inventario.id_insumo_fk = Historico.id_insumo_fk
WHERE Insumo.estado = 1
GROUP BY Inventario.id_insumo_fk, Insumo.nombre_insumo, Inventario.stock_inventario;

-- SELECT * FROM VW_INVENTARIO_INSUMO;

/*-----------Inventario de producto-----------*/
CREATE VIEW VW_INVENTARIO_PRODUCTO AS 
SELECT Inventario.id_producto_fk AS ID,
    Producto.nombre_producto AS PRODUCTO,
    SUM(IF(Historico.id_tipo_movimiento_fk = 1, Historico.cantidad_historico, 0)) AS ENTRADAS,
    SUM(IF(Historico.id_tipo_movimiento_fk = 2, Historico.cantidad_historico, 0)) AS SALIDAS,
    Inventario.stock_inventario AS STOCK
FROM Inventario
INNER JOIN Producto ON Inventario.id_producto_fk = Producto.id_producto
INNER JOIN Historico ON Inventario.id_producto_fk = Historico.id_producto_fk
WHERE Producto.estado = 1
GROUP BY Inventario.id_producto_fk, Producto.nombre_producto, Inventario.stock_inventario;

-- SELECT * FROM VW_INVENTARIO_PRODUCTO;

/*--------Pedidos No finalizados-------*/
CREATE VIEW VW_PEDIDOS_NO_FINALIZADOS AS
SELECT p.id_pedido AS ID_PEDIDO, p.descripcion_pedido AS DESCRIPCION, p.fecha_pedido AS FECHA,
    e.nombre_estado AS ESTADO, u.no_documento_usuario AS DOC_USUARIO, u.celular_usuario AS CELULAR,
    CONCAT(u.nombre_usuario, ' ', u.apellido_usuario) AS CLIENTE
FROM pedido AS p
INNER JOIN estado_pedido AS e ON p.id_estado_pedido_fk = e.id_estado_pedido
INNER JOIN usuario AS u ON p.no_documento_usuario_fk = u.no_documento_usuario
WHERE e.nombre_estado != "Finalizados"
AND e.nombre_estado != "Cancelado"
AND p.estado = 1
ORDER BY p.fecha_pedido ASC;

-- SELECT * FROM VW_PEDIDOS_NO_FINALIZADOS;

/*--------Pedidos Finalizados-------*/
CREATE VIEW VW_PEDIDOS_FINALIZADOS AS
SELECT p.id_pedido AS ID_PEDIDO, p.descripcion_pedido AS DESCRIPCION, p.fecha_pedido AS FECHA,
    e.nombre_estado AS ESTADO, u.no_documento_usuario AS DOC_USUARIO, u.celular_usuario AS CELULAR,
    CONCAT(u.nombre_usuario, ' ', u.apellido_usuario) AS CLIENTE
FROM pedido AS p
INNER JOIN estado_pedido AS e ON p.id_estado_pedido_fk = e.id_estado_pedido
INNER JOIN usuario AS u ON p.no_documento_usuario_fk = u.no_documento_usuario
WHERE e.nombre_estado = "Finalizados"
OR e.nombre_estado = "Cancelado" -- Corregí la agrupación de condiciones lógicas
AND p.estado = 1
ORDER BY p.fecha_pedido ASC;


-- SELECT * FROM VW_PEDIDOS_FINALIZADOS;

/*------Listado de los proveedores con promedio de calificación-------*/
CREATE VIEW VW_PROVEEDORES_CALIFICACION_AVG AS 
SELECT proveedor.id_proveedor AS ID_PROVEEDOR, proveedor.empresa_proveedor AS EMPRESA,
    AVG(calificacion.estrellas_calificacion) AS PROMEDIO_CALIFICACION -- Cambié estrallas_calificacion a estrellas_calificacion
FROM proveedor
LEFT JOIN calificacion ON proveedor.id_proveedor = calificacion.id_proveedor_fk
WHERE proveedor.estado = 1
GROUP BY proveedor.id_proveedor, proveedor.empresa_proveedor;

-- SELECT * FROM VW_PROVEEDORES_CALIFICACION_AVG;

/*------Listado de ventas con su total y vendedor que la realizó-------*/
CREATE VIEW VW_DATOS_VENTA AS 
SELECT venta.id_venta AS ID, venta.fecha_venta AS FECHA, venta.hora_venta AS HORA, 
    venta.total_venta AS TOTAL, CONCAT(usuario.nombre_usuario, ' ', usuario.apellido_usuario) AS VENDEDOR
FROM venta
INNER JOIN usuario ON venta.no_documento_usuario_fk = usuario.no_documento_usuario;

-- SELECT * FROM VW_DATOS_VENTA;
