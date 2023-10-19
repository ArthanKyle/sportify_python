import mysql.connector
from mysql.connector import pooling
import os


db_config = {
    "host": os.getenv("MYSQL_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("MYSQL_DB"),
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db_config)
connection = connection_pool.get_connection()
connection.close()
