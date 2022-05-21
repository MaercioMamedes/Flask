from flask import Flask
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

from views.viewTemplate import *
from views.viewHome import *
from views.viewUserRegister import *
from views.viewPorfolio import *


if __name__ == "__main__":
    app.run(debug=True)
