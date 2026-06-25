from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import login_requerido, admin_requerido
from controllers.usuarios_controller import UsuariosController
from models.usuario import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios")
@admin_requerido
def listar():
    usuarios = UsuariosController.listar()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@usuarios_bp.route("/usuarios/nuevo", methods=["GET", "POST"])
@admin_requerido
def nuevo():
    if request.method == "POST":
        try:
            UsuariosController.crear(request.form)
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("usuarios.listar"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("usuarios/formulario.html", usuario=None)


@usuarios_bp.route("/usuarios/<int:id_usuario>/editar", methods=["GET", "POST"])
@admin_requerido
def editar(id_usuario):
    usuario = Usuario.obtener_por_id(id_usuario)
    if not usuario:
        flash("Usuario no encontrado.", "warning")
        return redirect(url_for("usuarios.listar"))

    if request.method == "POST":
        try:
            UsuariosController.actualizar(id_usuario, request.form)
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuarios.listar"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    return render_template("usuarios/formulario.html", usuario=usuario)


@usuarios_bp.route("/usuarios/<int:id_usuario>/eliminar", methods=["POST"])
@admin_requerido
def eliminar(id_usuario):
    if id_usuario == session.get("usuario_id"):
        flash("No puedes eliminar tu propio usuario mientras tienes sesión activa.", "warning")
        return redirect(url_for("usuarios.listar"))
    UsuariosController.eliminar(id_usuario)
    flash("Usuario eliminado correctamente.", "info")
    return redirect(url_for("usuarios.listar"))
