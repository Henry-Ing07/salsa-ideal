import json
from models.producto import Producto
from models.venta import Venta


class VentasController:

    @staticmethod
    def buscar_producto_para_venta(producto_id):
        return Producto.obtener_por_id(producto_id)

    @staticmethod
    def procesar_venta_form(form, usuario_id):
        """
        Espera del formulario:
        - cliente
        - items_json: JSON con lista de {producto_id, cantidad, precio}
        - descuento
        """
        cliente = form.get("cliente", "").strip() or "Cliente General"
        descuento = float(form.get("descuento", 0) or 0)
        items_raw = form.get("items_json", "[]")
        items = json.loads(items_raw)

        if not items:
            raise ValueError("El carrito está vacío. Agrega al menos un producto.")

        # Validar stock disponible antes de confirmar
        for item in items:
            producto = Producto.obtener_por_id(item["producto_id"])
            if not producto:
                raise ValueError("Uno de los productos ya no existe.")
            if producto["stock"] < float(item["cantidad"]):
                raise ValueError(
                    f"Stock insuficiente para '{producto['nombre']}'. "
                    f"Disponible: {producto['stock']}"
                )

        venta_id = Venta.crear_venta(
            cliente=cliente, items=items, descuento=descuento, usuario_id=usuario_id
        )
        return venta_id

    @staticmethod
    def historial(filtros):
        return Venta.historial(
            fecha_inicio=filtros.get("fecha_inicio"),
            fecha_fin=filtros.get("fecha_fin"),
            busqueda=filtros.get("busqueda"),
        )

    @staticmethod
    def detalle(venta_id):
        venta = Venta.obtener_por_id(venta_id)
        items = Venta.detalle_de_venta(venta_id)
        return venta, items
