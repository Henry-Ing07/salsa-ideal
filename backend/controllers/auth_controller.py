from functools import wraps
from flask import session, redirect, url_for, flash
from models.usuario import Usuario


def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorada


def admin_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("rol") != "Administrador":
            flash("No tienes permisos para acceder a esta sección.", "danger")
            return redirect(url_for("dashboard.index"))
        return f(*args, **kwargs)

    return decorada


class AuthController:

    @staticmethod
    def autenticar(usuario, contrasena):
        registro = Usuario.obtener_por_usuario(usuario)
        if not registro:
            return None
        if Usuario.verificar_contrasena(registro["contrasena"], contrasena):
            return registro
        return None

    @staticmethod
    def iniciar_sesion(registro):
        session.clear()
        session["usuario_id"] = registro["id"]
        session["nombre"] = registro["nombre"]
        session["rol"] = registro["rol"]
        session.permanent = True

    @staticmethod
    def cerrar_sesion():
        session.clear()
