from models.db import get_connection


class Producto:

    @staticmethod
    def listar(filtro_categoria=None, busqueda=None, solo_activos=True):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM productos WHERE 1=1"
                params = []
                if solo_activos:
                    sql += " AND activo = 1"
                if filtro_categoria:
                    sql += " AND categoria = %s"
                    params.append(filtro_categoria)
                if busqueda:
                    sql += " AND nombre LIKE %s"
                    params.append(f"%{busqueda}%")
                sql += " ORDER BY nombre ASC"
                cur.execute(sql, params)
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_producto):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def categorias():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT DISTINCT categoria FROM productos WHERE activo=1 ORDER BY categoria"
                )
                return [r["categoria"] for r in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def crear(nombre, descripcion, categoria, precio, stock, stock_minimo):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO productos (nombre, descripcion, categoria, precio, stock, stock_minimo) "
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (nombre, descripcion, categoria, precio, stock, stock_minimo),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_producto, nombre, descripcion, categoria, precio, stock, stock_minimo):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE productos SET nombre=%s, descripcion=%s, categoria=%s, "
                    "precio=%s, stock=%s, stock_minimo=%s WHERE id=%s",
                    (nombre, descripcion, categoria, precio, stock, stock_minimo, id_producto),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_producto):
        """Eliminación lógica para no perder historial de ventas asociado."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE productos SET activo = 0 WHERE id = %s", (id_producto,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def descontar_stock(id_producto, cantidad, cursor):
        """Se ejecuta dentro de una transacción de venta (recibe cursor externo)."""
        cursor.execute(
            "UPDATE productos SET stock = stock - %s WHERE id = %s", (cantidad, id_producto)
        )

    @staticmethod
    def stock_bajo():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM productos WHERE activo=1 AND stock <= stock_minimo "
                    "ORDER BY stock ASC"
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def contar_total():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS total FROM productos WHERE activo=1")
                return cur.fetchone()["total"]
        finally:
            conn.close()

    @staticmethod
    def contar_bajo_stock():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) AS total FROM productos WHERE activo=1 AND stock <= stock_minimo"
                )
                return cur.fetchone()["total"]
        finally:
            conn.close()

    @staticmethod
    def mas_vendidos(limite=5):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.nombre, SUM(dv.cantidad) AS unidades
                    FROM detalle_ventas dv
                    JOIN productos p ON p.id = dv.producto_id
                    GROUP BY p.id, p.nombre
                    ORDER BY unidades DESC
                    LIMIT %s
                    """,
                    (limite,),
                )
                return cur.fetchall()
        finally:
            conn.close()
