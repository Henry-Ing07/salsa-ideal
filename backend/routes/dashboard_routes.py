from flask import Blueprint, render_template, jsonify, request
from controllers.auth_controller import login_requerido
from models.producto import Producto
from models.venta import Venta

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_requerido
def index():
    total_productos = Producto.contar_total()
    bajo_stock = Producto.contar_bajo_stock()
    ventas_dia = Venta.ventas_del_dia()
    ventas_mes = Venta.ventas_del_mes()
    productos_bajo_stock = Producto.stock_bajo()

    return render_template(
        "dashboard.html",
        total_productos=total_productos,
        bajo_stock=bajo_stock,
        ventas_dia=ventas_dia,
        ventas_mes=ventas_mes,
        productos_bajo_stock=productos_bajo_stock,
    )


DIAS_ES = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo",
}
MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
    "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
    "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
}

@dashboard_bp.route("/dashboard/api/ventas-por-mes")
@login_requerido
def api_ventas_por_mes():
    vista = request.args.get("periodo", "anio")
    if vista == "semana":
        datos = Venta.ventas_semana_actual()
        resultado = [{"periodo": DIAS_ES.get(d["dia_nombre"], d["dia_nombre"]), "total": float(d["total"] or 0)} for d in datos]
    elif vista == "mes":
        datos = Venta.ventas_mes_actual()
        resultado = [{"periodo": str(d["dia_num"]), "total": float(d["total"] or 0)} for d in datos]
    else:
        datos = Venta.ventas_anio_actual()
        resultado = [{"periodo": MESES_ES.get(d["mes_nombre"], d["mes_nombre"]), "total": float(d["total"] or 0)} for d in datos]
    return jsonify(resultado)


@dashboard_bp.route("/dashboard/api/mas-vendidos")
@login_requerido
def api_mas_vendidos():
    datos = Producto.mas_vendidos(limite=5)
    return jsonify([
        {"nombre": d["nombre"], "unidades": int(d["unidades"] or 0)} for d in datos
    ])
