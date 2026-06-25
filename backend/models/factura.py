from models.db import get_connection


class Factura:

    @staticmethod
    def obtener_por_venta(venta_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM facturas WHERE venta_id = %s", (venta_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(factura_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT f.*, v.cliente, v.subtotal, v.descuento, v.total, v.fecha AS fecha_venta,
                           u.nombre AS vendedor_nombre, u.rol AS vendedor_rol
                    FROM facturas f
                    JOIN ventas v ON v.id = f.venta_id
                    LEFT JOIN usuarios u ON u.id = v.usuario_id
                    WHERE f.id = %s
                    """,
                    (factura_id,),
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT f.id, f.numero_factura, f.fecha, v.cliente, v.total
                    FROM facturas f
                    JOIN ventas v ON v.id = f.venta_id
                    ORDER BY f.fecha DESC
                    """
                )
                return cur.fetchall()
        finally:
            conn.close()
