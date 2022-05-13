import os

SECRET_KEY = 'alura'
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_UNIX_SOCKET = "/opt/lampp/var/mysql/mysql.sock"
MYSQL_DB = "GameDataBase"
MYSQL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/medias'
