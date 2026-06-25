from datetime import datetime, date
from models.db import get_connection
from models.producto import Producto


class Venta:

    @staticmethod
    def crear_venta(cliente, items, descuento, usuario_id):
        """
        items: lista de dicts [{producto_id, cantidad, precio}]
        Crea la venta, el detalle, descuenta stock y retorna el id de venta.
        Todo dentro de una transacción.
        """
        subtotal = sum(item["cantidad"] * item["precio"] for item in items)
        total = subtotal - descuento
        if total < 0:
            total = 0

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO ventas (cliente, subtotal, descuento, total, usuario_id) "
                    "VALUES (%s,%s,%s,%s,%s)",
                    (cliente, subtotal, descuento, total, usuario_id),
                )
                venta_id = cur.lastrowid

                for item in items:
                    cur.execute(
                        "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio) "
                        "VALUES (%s,%s,%s,%s)",
                        (venta_id, item["producto_id"], item["cantidad"], item["precio"]),
                    )
                    Producto.descontar_stock(item["producto_id"], item["cantidad"], cur)

                numero_factura = f"FAC-{venta_id:06d}"
                cur.execute(
                    "INSERT INTO facturas (venta_id, numero_factura) VALUES (%s,%s)",
                    (venta_id, numero_factura),
                )

            conn.commit()
            return venta_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(venta_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM ventas WHERE id = %s", (venta_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def detalle_de_venta(venta_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT dv.*, p.nombre AS producto_nombre
                    FROM detalle_ventas dv
                    JOIN productos p ON p.id = dv.producto_id
                    WHERE dv.venta_id = %s
                    """,
                    (venta_id,),
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def historial(filtro=None, fecha_inicio=None, fecha_fin=None, busqueda=None):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                sql = (
                    "SELECT v.*, u.nombre AS vendedor "
                    "FROM ventas v LEFT JOIN usuarios u ON u.id = v.usuario_id WHERE 1=1"
                )
                params = []

                if fecha_inicio:
                    sql += " AND v.fecha >= %s"
                    params.append(fecha_inicio)
                if fecha_fin:
                    sql += " AND v.fecha <= %s"
                    params.append(fecha_fin)
                if busqueda:
                    sql += " AND v.cliente LIKE %s"
                    params.append(f"%{busqueda}%")

                sql += " ORDER BY v.fecha DESC"
                cur.execute(sql, params)
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def ventas_del_dia():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) AS total, COALESCE(SUM(total),0) AS ingresos "
                    "FROM ventas WHERE DATE(fecha) = CURDATE()"
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def ventas_del_mes():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) AS total, COALESCE(SUM(total),0) AS ingresos "
                    "FROM ventas WHERE YEAR(fecha)=YEAR(CURDATE()) AND MONTH(fecha)=MONTH(CURDATE())"
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def ventas_semana_actual():
        """Lunes a domingo de la semana en curso, un registro por día."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DATE_FORMAT(fecha, '%Y-%m-%d') AS periodo,
                           DAYNAME(fecha) AS dia_nombre,
                           COALESCE(SUM(total), 0) AS total
                    FROM ventas
                    WHERE YEARWEEK(fecha, 1) = YEARWEEK(CURDATE(), 1)
                    GROUP BY periodo, dia_nombre
                    ORDER BY periodo ASC
                    """
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def ventas_mes_actual():
        """Un registro por día del mes en curso."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DATE_FORMAT(fecha, '%Y-%m-%d') AS periodo,
                           DAY(fecha) AS dia_num,
                           COALESCE(SUM(total), 0) AS total
                    FROM ventas
                    WHERE YEAR(fecha) = YEAR(CURDATE())
                      AND MONTH(fecha) = MONTH(CURDATE())
                    GROUP BY periodo, dia_num
                    ORDER BY periodo ASC
                    """
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def ventas_anio_actual():
        """Un registro por mes del año en curso."""
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DATE_FORMAT(fecha, '%Y-%m') AS periodo,
                           MONTHNAME(fecha) AS mes_nombre,
                           COALESCE(SUM(total), 0) AS total
                    FROM ventas
                    WHERE YEAR(fecha) = YEAR(CURDATE())
                    GROUP BY periodo, mes_nombre
                    ORDER BY periodo ASC
                    """
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def ventas_por_mes(meses=6):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DATE_FORMAT(fecha, '%%Y-%%m') AS periodo, SUM(total) AS total
                    FROM ventas
                    WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
                    GROUP BY periodo
                    ORDER BY periodo ASC
                    """,
                    (meses,),
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def reporte_ganancias(periodo="mensual"):
        """periodo: diario | semanal | mensual"""
        formato = {
            "diario": "%Y-%m-%d",
            "semanal": "%x-%v",
            "mensual": "%Y-%m",
        }.get(periodo, "%Y-%m")

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT DATE_FORMAT(fecha, '{formato}') AS periodo,
                           COUNT(*) AS num_ventas,
                           SUM(total) AS total
                    FROM ventas
                    GROUP BY periodo
                    ORDER BY periodo DESC
                    LIMIT 24
                    """
                )
                return cur.fetchall()
        finally:
            conn.close()
