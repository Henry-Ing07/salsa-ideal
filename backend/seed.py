"""
Script de inicialización.

Ejecutar UNA SOLA VEZ después de crear la base de datos con database/salsa_ideal.sql,
para establecer correctamente la contraseña del usuario administrador por defecto
(la tabla se crea con un valor temporal 'PENDIENTE_HASH').

Uso:
    cd backend
    python seed.py
"""
from werkzeug.security import generate_password_hash
from models.db import get_connection


def main():
    nueva_clave = "admin123"
    hash_clave = generate_password_hash(nueva_clave)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE usuarios SET contrasena = %s WHERE usuario = 'admin'",
                (hash_clave,),
            )
        conn.commit()
        print("Listo. Usuario: admin | Contraseña: admin123")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
