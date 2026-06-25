from flask import Flask, session
from datetime import datetime

from config import Config

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.inventario_routes import inventario_bp
from routes.ventas_routes import ventas_bp
from routes.facturas_routes import facturas_bp
from routes.reportes_routes import reportes_bp
from routes.usuarios_routes import usuarios_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.template_filter("moneda")
    def filtro_moneda(valor):
        try:
            valor = float(valor or 0)
        except (TypeError, ValueError):
            valor = 0.0
        entero, _ = f"{valor:,.2f}".split(".")
        return entero.replace(",", ".")

    # Registro de blueprints (módulos)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(usuarios_bp)

    @app.context_processor
    def inject_globals():
        return {
            "session_usuario": session.get("nombre"),
            "session_rol": session.get("rol"),
            "anio_actual": datetime.now().year,
            "empresa_nombre": Config.EMPRESA_NOMBRE,
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
