-- ============================================================
-- Base de datos: salsa_ideal
-- Sistema Web para el Control de Inventario y Ventas
-- Negocio: Salsa Marca Ideal
-- ============================================================

CREATE DATABASE IF NOT EXISTS salsa_ideal
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE salsa_ideal;

-- ------------------------------------------------------------
-- Tabla: usuarios
-- ------------------------------------------------------------
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Vendedor') NOT NULL DEFAULT 'Vendedor',
    activo TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: productos
-- ------------------------------------------------------------
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 5,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: ventas
-- ------------------------------------------------------------
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente VARCHAR(150) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
    descuento DECIMAL(10,2) NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    usuario_id INT,
    CONSTRAINT fk_ventas_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: detalle_ventas
-- ------------------------------------------------------------
CREATE TABLE detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_detalle_venta FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (producto_id) REFERENCES productos(id)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: facturas
-- ------------------------------------------------------------
CREATE TABLE facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    numero_factura VARCHAR(30) NOT NULL UNIQUE,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_factura_venta FOREIGN KEY (venta_id) REFERENCES ventas(id)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Datos iniciales
-- ------------------------------------------------------------

-- Usuario administrador por defecto
-- Usuario: admin   Contraseña: admin123
-- (el hash se genera al primer arranque mediante seed.py, ver README)
INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES
('Administrador General', 'admin', 'PENDIENTE_HASH', 'Administrador');

-- Productos de ejemplo
INSERT INTO productos (nombre, descripcion, categoria, precio, stock, stock_minimo) VALUES
('Salsa Ideal Picante 250ml', 'Salsa picante tradicional, botella de 250ml', 'Picante', 4500.00, 120, 20),
('Salsa Ideal BBQ 350ml', 'Salsa BBQ ahumada, botella de 350ml', 'BBQ', 6200.00, 80, 15),
('Salsa Ideal Tomate 500ml', 'Salsa de tomate clasica, botella de 500ml', 'Tomate', 5300.00, 4, 20),
('Salsa Ideal Ajo 200ml', 'Salsa de ajo cremosa, botella de 200ml', 'Cremas', 3900.00, 0, 10),
('Salsa Ideal Mango Habanero 250ml', 'Salsa agridulce picante, botella de 250ml', 'Picante', 5100.00, 45, 10);

-- ------------------------------------------------------------
-- Indices recomendados
-- ------------------------------------------------------------
CREATE INDEX idx_productos_categoria ON productos(categoria);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_detalle_venta ON detalle_ventas(venta_id);
