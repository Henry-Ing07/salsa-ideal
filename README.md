# Sistema Web para el Control de Inventario y Ventas — Salsa Marca Ideal

Sistema web completo (tipo ERP) para automatizar el inventario, las ventas y la
facturación del negocio **Salsa Marca Ideal**, reemplazando el manejo manual en
Excel/WhatsApp.

**Stack:** HTML5 + CSS3 + JavaScript + Bootstrap 5 (frontend) · Python Flask (backend) · MySQL (base de datos).

---

## 1. Requisitos previos

- Python 3.10 o superior instalado.
- Un servidor MySQL. Como no tienes MySQL instalado, la opción más simple es **XAMPP**:

### Instalar XAMPP (incluye MySQL/MariaDB + phpMyAdmin)

1. Descarga XAMPP para tu sistema operativo desde: https://www.apachefriends.org/es/index.html
2. Instálalo (en Windows, deja las opciones por defecto; en Mac/Linux sigue el instalador).
3. Abre el **Panel de Control de XAMPP** y da clic en **Start** junto a **MySQL** (y Apache, si quieres usar phpMyAdmin).
4. Con esto ya tienes MySQL corriendo en `localhost:3306`, usuario `root` y **sin contraseña** (configuración por defecto de XAMPP).

> Si prefieres instalar MySQL Server directamente (sin XAMPP), también funciona: https://dev.mysql.com/downloads/installer/

---

## 2. Crear la base de datos

1. Abre **phpMyAdmin** (en XAMPP: botón "Admin" junto a MySQL, o ve a `http://localhost/phpmyadmin`) **o** usa la consola de MySQL.
2. Importa el archivo `database/salsa_ideal.sql`:
   - **Desde phpMyAdmin:** pestaña "Importar" → selecciona `database/salsa_ideal.sql` → "Continuar". Esto crea la base `salsa_ideal` con todas las tablas y datos de ejemplo.
   - **Desde la terminal:**
     ```bash
     mysql -u root -p < database/salsa_ideal.sql
     ```
     (con XAMPP por defecto no hay contraseña, así que sería `mysql -u root < database/salsa_ideal.sql`)

---

## 3. Configurar el proyecto

1. Abre la carpeta `salsa-ideal/` en Visual Studio Code.
2. Crea un entorno virtual e instala dependencias:

   ```bash
   cd backend
   python -m venv venv

   # Activar entorno virtual:
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

   pip install -r ../requirements.txt
   ```

3. Si tu MySQL tiene usuario/contraseña distintos a `root` sin clave, edita las
   variables de entorno o directamente el archivo `backend/config.py`:

   ```python
   MYSQL_HOST = "localhost"
   MYSQL_USER = "root"
   MYSQL_PASSWORD = ""        # tu contraseña de MySQL si tienes una
   MYSQL_DB = "salsa_ideal"
   ```

4. **Genera la contraseña del usuario administrador** (paso obligatorio, una sola vez):

   ```bash
   python seed.py
   ```

   Esto deja listo el usuario:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

---

## 4. Ejecutar el sistema

```bash
python app.py
```

Abre tu navegador en: **http://localhost:5000**

Inicia sesión con `admin` / `admin123`.

---

## 5. Estructura del proyecto

```text
salsa-ideal/
│
├── backend/
│   ├── app.py              # Punto de entrada Flask
│   ├── config.py           # Configuración (BD, sesiones, datos empresa)
│   ├── seed.py              # Script para inicializar la clave del admin
│   ├── models/              # Acceso a datos (usuarios, productos, ventas, facturas)
│   ├── routes/               # Blueprints (rutas) por módulo
│   ├── controllers/         # Lógica de negocio por módulo
│   ├── static/
│   │   ├── css/style.css     # Tema visual "Esmeralda y Oro" con colores de marca Ideal
│   │   ├── js/pos.js         # Lógica del carrito de ventas (POS)
│   │   └── img/logo-ideal.png
│   └── templates/            # Vistas HTML (Jinja2)
│
├── database/
│   └── salsa_ideal.sql       # Script completo de la base de datos
│
├── requirements.txt
└── README.md
```

---

## 6. Módulos incluidos

1. **Login** — autenticación con sesiones Flask, hash de contraseñas (Werkzeug), mostrar/ocultar contraseña.
2. **Dashboard** — KPIs (productos, bajo stock, ventas del día/mes) y gráficas con Chart.js (ventas por mes, productos más vendidos).
3. **Inventario** — CRUD completo, búsqueda, filtro por categoría, alertas de stock bajo/agotado.
4. **Ventas (POS)** — carrito de compras interactivo, descuentos, cálculo automático, descuento automático de stock al confirmar.
5. **Facturación** — generación automática de número de factura, vista imprimible y descarga en PDF (ReportLab).
6. **Historial de ventas** — filtros por fecha y cliente.
7. **Reportes** — inventario (disponibles/bajo stock/agotados) y ventas/ganancias (diario/semanal/mensual), exportables a **Excel** y **PDF**.
8. **Usuarios** — roles Administrador (acceso total) y Vendedor (inventario + ventas), solo accesible para Administradores.

---

## 7. Seguridad implementada

- Hash de contraseñas con Werkzeug (`generate_password_hash` / `check_password_hash`).
- Sesiones de Flask protegidas con `SECRET_KEY`.
- Decoradores `@login_requerido` y `@admin_requerido` que protegen cada ruta según el rol.
- Todas las consultas usan parámetros (`%s`) en lugar de concatenar texto, evitando inyección SQL.
- Validaciones de stock disponible antes de confirmar cualquier venta.

---

## 8. Comprimir el proyecto en ZIP

Desde la carpeta que contiene `salsa-ideal/`:

```bash
# Windows (PowerShell)
Compress-Archive -Path salsa-ideal -DestinationPath salsa-ideal.zip

# Mac/Linux
zip -r salsa-ideal.zip salsa-ideal
```

Luego puedes abrir ese ZIP, descomprimirlo y abrir la carpeta `salsa-ideal` en Visual Studio Code.

---

## 9. Notas finales

- Los datos de ejemplo de productos en `salsa_ideal.sql` ya incluyen un producto agotado y uno con stock bajo, para que veas las alertas funcionando desde el primer arranque.
- Puedes cambiar el nombre, NIT y dirección de la empresa que aparecen en las facturas editando `Config.EMPRESA_NOMBRE`, `EMPRESA_NIT` y `EMPRESA_DIRECCION` en `backend/config.py`.
- El logo usado en el sistema (`backend/static/img/logo-ideal.png`) es el logo oficial de la marca Ideal.
