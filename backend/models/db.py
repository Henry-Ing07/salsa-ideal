import pymysql
from pymysql.cursors import DictCursor
from config import Config


def get_connection():
    """
    Crea y retorna una nueva conexión a MySQL.
    Se usa una conexión nueva por petición para evitar problemas de hilos.
    """
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=DictCursor,
        autocommit=False,
        charset="utf8mb4",
    )
