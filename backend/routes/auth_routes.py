from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController, login_requerido

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def raiz():
    if "usuario_id" in session:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()

        registro = AuthController.autenticar(usuario, contrasena)
        if registro:
            AuthController.iniciar_sesion(registro)
            flash(f"Bienvenido, {registro['nombre']}.", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_requerido
def logout():
    AuthController.cerrar_sesion()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
