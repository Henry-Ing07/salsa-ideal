from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from controllers.auth_controller import login_requerido, admin_requerido
from controllers.facturas_controller import FacturasController
from models.factura import Factura
from models.venta import Venta as VentaModel

facturas_bp = Blueprint("facturas", __name__)


@facturas_bp.route("/facturas")
@login_requerido
def listar():
    facturas = FacturasController.listar()
    return render_template("facturas/listar.html", facturas=facturas)


@facturas_bp.route("/facturas/<int:factura_id>")
@login_requerido
def ver(factura_id):
    factura = FacturasController.obtener(factura_id)
    if not factura:
        flash("Factura no encontrada.", "warning")
        return redirect(url_for("facturas.listar"))
    factura["items"] = VentaModel.detalle_de_venta(factura["venta_id"])
    return render_template("facturas/ver.html", factura=factura)


@facturas_bp.route("/facturas/<int:factura_id>/eliminar", methods=["POST"])
@admin_requerido
def eliminar(factura_id):
    try:
        factura = FacturasController.obtener(factura_id)
        if not factura:
            flash("Factura no encontrada.", "warning")
            return redirect(url_for("facturas.listar"))
        VentaModel.eliminar(factura["venta_id"])
        flash("Factura y venta eliminadas correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar: {e}", "danger")
    return redirect(url_for("facturas.listar"))


@facturas_bp.route("/facturas/venta/<int:venta_id>")
@login_requerido
def ver_por_venta(venta_id):
    factura = Factura.obtener_por_venta(venta_id)
    if not factura:
        flash("No se encontró la factura para esta venta.", "warning")
        return redirect(url_for("ventas.historial"))
    return redirect(url_for("facturas.ver", factura_id=factura["id"]))


@facturas_bp.route("/facturas/<int:factura_id>/pdf")
@login_requerido
def descargar_pdf(factura_id):
    buffer = FacturasController.generar_pdf(factura_id)
    if not buffer:
        flash("Factura no encontrada.", "warning")
        return redirect(url_for("facturas.listar"))
    factura = FacturasController.obtener(factura_id)
    nombre_archivo = f"{factura['numero_factura']}.pdf"
    return send_file(
        buffer, as_attachment=True, download_name=nombre_archivo,
        mimetype="application/pdf",
    )
