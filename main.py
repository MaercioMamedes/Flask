from flask import *
from model.models import *
from dataBase.conectDataBase import *
import pandas as pd

app = Flask(__name__)
app.secret_key = 'alura'
lista = ['Maercio', 'Joséas', 'Jamerson', 'Emanoel']
reader_data_base()


@app.route('/')
def index():
    return render_template('index.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa', users=lista)


@app.route('/portfolio')
def portfolio():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?proxima=portfolio')
    return render_template('portfolio.html', title='Cadastro de Ativos', title_page='Portfólio')


@app.route('/register')
def register_user():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?proxima=register')
    return render_template('registerUser.html', title_page='Cadastro de usuário', title='Cadastro')


@app.route('/user', methods=['POST'])
def user():
    new_user = request.form['nome']
    lista.append(new_user)

    return redirect('/')


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', title_page='Login de Usuário', title='Login', proxima=proxima)


@app.route('/auth', methods=['POST', ])
def auth():
    if 'master' == request.form['password'] and request.form['user'] in lista:
        session['user_logged'] = request.form['user']
        flash(request.form['user'] + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        print(f'{proxima_pagina}')
        return redirect(f'/{proxima_pagina}')

    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)
