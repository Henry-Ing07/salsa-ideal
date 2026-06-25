from models.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:

    @staticmethod
    def obtener_por_usuario(usuario):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM usuarios WHERE usuario = %s AND activo = 1", (usuario,)
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, nombre, usuario, rol, activo, fecha_creacion "
                    "FROM usuarios ORDER BY id DESC"
                )
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def crear(nombre, usuario, contrasena_plana, rol):
        hash_pass = generate_password_hash(contrasena_plana)
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (nombre, usuario, contrasena, rol) "
                    "VALUES (%s, %s, %s, %s)",
                    (nombre, usuario, hash_pass, rol),
                )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_usuario, nombre, rol, activo, nueva_contrasena=None):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                if nueva_contrasena:
                    hash_pass = generate_password_hash(nueva_contrasena)
                    cur.execute(
                        "UPDATE usuarios SET nombre=%s, rol=%s, activo=%s, contrasena=%s "
                        "WHERE id=%s",
                        (nombre, rol, activo, hash_pass, id_usuario),
                    )
                else:
                    cur.execute(
                        "UPDATE usuarios SET nombre=%s, rol=%s, activo=%s WHERE id=%s",
                        (nombre, rol, activo, id_usuario),
                    )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_usuario):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def verificar_contrasena(hash_guardado, contrasena_plana):
        return check_password_hash(hash_guardado, contrasena_plana)
