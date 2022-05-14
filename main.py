from helpers import *
from flask import *
from model.models import *
from flask_mysqldb import *
from model.b3 import *
from dao import PortfolioDao, UserDao


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MySQL(app)
portfolio_dao = PortfolioDao(db)
user_dao = UserDao(db)
repository = Repository()

from views import *


if __name__ == "__main__":
    app.run(debug=True)
