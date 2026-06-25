from models.producto import Producto


class InventarioController:

    @staticmethod
    def listar_productos(categoria=None, busqueda=None):
        return Producto.listar(filtro_categoria=categoria, busqueda=busqueda)

    @staticmethod
    def obtener(id_producto):
        return Producto.obtener_por_id(id_producto)

    @staticmethod
    def categorias():
        return Producto.categorias()

    @staticmethod
    def crear_producto(form):
        Producto.crear(
            nombre=form.get("nombre", "").strip(),
            descripcion=form.get("descripcion", "").strip(),
            categoria=form.get("categoria", "").strip(),
            precio=float(form.get("precio", 0) or 0),
            stock=int(form.get("stock", 0) or 0),
            stock_minimo=int(form.get("stock_minimo", 0) or 0),
        )

    @staticmethod
    def actualizar_producto(id_producto, form):
        Producto.actualizar(
            id_producto=id_producto,
            nombre=form.get("nombre", "").strip(),
            descripcion=form.get("descripcion", "").strip(),
            categoria=form.get("categoria", "").strip(),
            precio=float(form.get("precio", 0) or 0),
            stock=int(form.get("stock", 0) or 0),
            stock_minimo=int(form.get("stock_minimo", 0) or 0),
        )

    @staticmethod
    def eliminar_producto(id_producto):
        Producto.eliminar(id_producto)

    @staticmethod
    def estado_stock(producto):
        if producto["stock"] <= 0:
            return "agotado"
        if producto["stock"] <= producto["stock_minimo"]:
            return "bajo"
        return "ok"
