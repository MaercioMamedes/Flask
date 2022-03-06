from sqlite3 import *


def reader_data_base():
    conector = connect("../AppDataBase.db")
    cursor = conector.cursor()

    """sql = "SELECT * FROM 'user'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conector.close()"""

