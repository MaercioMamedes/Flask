from flask import *
from model.models import *
from dataBase.conectDataBase import *
import pandas as pd

app = Flask(__name__)
lista = ['Maercio', 'Joséas', 'Jamerson', 'Emanoel']
reader_data_base()


@app.route('/')
def index():
    return render_template('index.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa',users=lista)


@app.route('/register')
def register_user():
    return render_template('registerUser.html',title_page='Cadastro de usuário',title='Cadastro')


@app.route('/user', methods=['POST'])
def user():
    new_user = request.form['nome']
    lista.append(new_user)

    return redirect('/')


app.run(debug=True)
