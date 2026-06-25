import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ideal-salsa-clave-secreta-2024")

    # MySQL - se sobreescribe con variables de entorno en Railway
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "canela07")
    MYSQL_DB = os.environ.get("MYSQL_DB", "salsa_ideal")

    # Sesiones
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(BASE_DIR, "flask_session")
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 4  # 4 horas

    # Facturación
    EMPRESA_NOMBRE = "Salsa Marca Ideal"
    EMPRESA_NIT = "900.000.000-1"
    EMPRESA_DIRECCION = "Cúcuta, Norte de Santander, Colombia"
