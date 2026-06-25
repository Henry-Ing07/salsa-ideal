from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.auth_controller import login_requerido
from controllers.inventario_controller import InventarioController

inventario_bp = Blueprint("inventario", __name__)


@inventario_bp.route("/inventario")
@login_requerido
def listar():
    categoria = request.args.get("categoria") or None
    busqueda = request.args.get("q") or None
    productos = InventarioController.listar_productos(categoria=categoria, busqueda=busqueda)
    categorias = InventarioController.categorias()
    return render_template(
        "inventario/listar.html",
        productos=productos,
        categorias=categorias,
        categoria_actual=categoria,
        busqueda=busqueda or "",
        estado_stock=InventarioController.estado_stock,
    )


@inventario_bp.route("/inventario/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    if request.method == "POST":
        try:
            InventarioController.crear_producto(request.form)
            flash("Producto registrado correctamente.", "success")
            return redirect(url_for("inventario.listar"))
        except Exception as e:
            flash(f"Error al registrar producto: {e}", "danger")
    return render_template("inventario/formulario.html", producto=None)


@inventario_bp.route("/inventario/<int:id_producto>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id_producto):
    producto = InventarioController.obtener(id_producto)
    if not producto:
        flash("Producto no encontrado.", "warning")
        return redirect(url_for("inventario.listar"))

    if request.method == "POST":
        try:
            InventarioController.actualizar_producto(id_producto, request.form)
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("inventario.listar"))
        except Exception as e:
            flash(f"Error al actualizar producto: {e}", "danger")

    return render_template("inventario/formulario.html", producto=producto)


@inventario_bp.route("/inventario/<int:id_producto>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id_producto):
    InventarioController.eliminar_producto(id_producto)
    flash("Producto eliminado correctamente.", "info")
    return redirect(url_for("inventario.listar"))
