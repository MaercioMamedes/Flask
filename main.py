from flask import *
from flask_mysqldb import MySQL
from model.b3 import *


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MySQL(app)
repository = Repository()

from views import *

if __name__ == "__main__":
    app.run(debug=True)
