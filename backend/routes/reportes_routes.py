from flask import Blueprint, render_template, request, send_file
from controllers.auth_controller import login_requerido
from controllers.reportes_controller import ReportesController

reportes_bp = Blueprint("reportes", __name__)


@reportes_bp.route("/reportes")
@login_requerido
def index():
    periodo = request.args.get("periodo", "mensual")
    inventario = ReportesController.reporte_inventario()
    ventas = ReportesController.reporte_ventas(periodo=periodo)
    return render_template(
        "reportes/index.html", inventario=inventario, ventas=ventas, periodo=periodo
    )


@reportes_bp.route("/reportes/inventario/excel")
@login_requerido
def inventario_excel():
    buffer = ReportesController.exportar_inventario_excel()
    return send_file(
        buffer, as_attachment=True, download_name="reporte_inventario.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@reportes_bp.route("/reportes/inventario/pdf")
@login_requerido
def inventario_pdf():
    buffer = ReportesController.exportar_inventario_pdf()
    return send_file(
        buffer, as_attachment=True, download_name="reporte_inventario.pdf",
        mimetype="application/pdf",
    )


@reportes_bp.route("/reportes/ventas/excel")
@login_requerido
def ventas_excel():
    periodo = request.args.get("periodo", "mensual")
    buffer = ReportesController.exportar_ventas_excel(periodo=periodo)
    return send_file(
        buffer, as_attachment=True, download_name="reporte_ventas.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@reportes_bp.route("/reportes/ventas/pdf")
@login_requerido
def ventas_pdf():
    periodo = request.args.get("periodo", "mensual")
    buffer = ReportesController.exportar_ventas_pdf(periodo=periodo)
    return send_file(
        buffer, as_attachment=True, download_name="reporte_ventas.pdf",
        mimetype="application/pdf",
    )
