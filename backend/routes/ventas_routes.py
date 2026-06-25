from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
)
from controllers.auth_controller import login_requerido, admin_requerido
from controllers.ventas_controller import VentasController
from controllers.inventario_controller import InventarioController
from models.producto import Producto
from models.venta import Venta

ventas_bp = Blueprint("ventas", __name__)


@ventas_bp.route("/ventas/nueva")
@login_requerido
def nueva():
    productos = InventarioController.listar_productos()
    return render_template("ventas/pos.html", productos=productos)


@ventas_bp.route("/ventas/api/producto/<int:id_producto>")
@login_requerido
def api_producto(id_producto):
    p = Producto.obtener_por_id(id_producto)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({
        "id": p["id"], "nombre": p["nombre"],
        "precio": float(p["precio"]), "stock": p["stock"],
    })


@ventas_bp.route("/ventas/registrar", methods=["POST"])
@login_requerido
def registrar():
    try:
        venta_id = VentasController.procesar_venta_form(request.form, session["usuario_id"])
        flash("Venta registrada y factura generada correctamente.", "success")
        return redirect(url_for("facturas.ver_por_venta", venta_id=venta_id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ventas.nueva"))
    except Exception as e:
        flash(f"Error al registrar la venta: {e}", "danger")
        return redirect(url_for("ventas.nueva"))


@ventas_bp.route("/ventas/historial")
@login_requerido
def historial():
    filtros = {
        "fecha_inicio": request.args.get("fecha_inicio") or None,
        "fecha_fin": request.args.get("fecha_fin") or None,
        "busqueda": request.args.get("q") or None,
    }
    ventas = VentasController.historial(filtros)
    return render_template("ventas/historial.html", ventas=ventas, filtros=filtros)


@ventas_bp.route("/ventas/<int:venta_id>")
@login_requerido
def detalle(venta_id):
    venta, items = VentasController.detalle(venta_id)
    if not venta:
        flash("Venta no encontrada.", "warning")
        return redirect(url_for("ventas.historial"))
    return render_template("ventas/detalle.html", venta=venta, items=items)


@ventas_bp.route("/ventas/<int:venta_id>/eliminar", methods=["POST"])
@admin_requerido
def eliminar(venta_id):
    try:
        Venta.eliminar(venta_id)
        flash("Venta eliminada correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar la venta: {e}", "danger")
    return redirect(url_for("ventas.historial"))
