from models.usuario import Usuario


class UsuariosController:

    @staticmethod
    def listar():
        return Usuario.listar()

    @staticmethod
    def crear(form):
        nombre = form.get("nombre", "").strip()
        usuario = form.get("usuario", "").strip()
        contrasena = form.get("contrasena", "").strip()
        rol = form.get("rol", "Vendedor")

        if not nombre or not usuario or not contrasena:
            raise ValueError("Todos los campos son obligatorios.")
        if Usuario.obtener_por_usuario(usuario):
            raise ValueError("Ese nombre de usuario ya existe.")

        Usuario.crear(nombre, usuario, contrasena, rol)

    @staticmethod
    def actualizar(id_usuario, form):
        nombre = form.get("nombre", "").strip()
        rol = form.get("rol", "Vendedor")
        activo = 1 if form.get("activo") == "on" else 0
        nueva_contrasena = form.get("contrasena", "").strip() or None

        Usuario.actualizar(id_usuario, nombre, rol, activo, nueva_contrasena)

    @staticmethod
    def eliminar(id_usuario):
        Usuario.eliminar(id_usuario)
