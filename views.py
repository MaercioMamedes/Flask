from dao import PortfolioDao, UserDao
from main import db, app
from time import time
from helpers import *
import datetime
import yfinance as yf
from model.models import User

portfolio_dao = PortfolioDao(db)
user_dao = UserDao(db)


@app.route('/')
def index():
    user_on = 'Ususário não logado' if 'user_logged' not in session else session['user_logged']
    users_list = user_dao.to_list()
    return render_template('index.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa',
                           user_logged=user_on,
                           users=users_list)


@app.route('/ranking')
def ranking_traders():
    return render_template('ranking.html', title='Classificação', title_page='Traders')


@app.route('/assets')
def assets():
    papel = yf.Ticker('MGLU3.SA')
    dados = papel.info
    chaves = list(dados.keys())
    valores = list(dados.values())

    lista = [[chaves[x], valores[x]] for x in range(len(chaves))]
    return render_template('assets.html', title='Ativos',
                           set_element=lista,
                           title_page='Ativos no Jogo')


@app.route('/cockpit')
def cockpit():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?proxima=cockpit')

    else:
        return render_template('cockpit.html', user_logged=session['user_logged'], title='Cockpoit do Trader',
                               title_page='Cockpit')


@app.route('/add-ticker', methods=['POST'])
def add_ticker():
    ticker = request.form['ticker']
    repository.download_b3(ticker.upper() + '.SA')
    lista = repository.list_asset
    return render_template('cockpit.html', user_logged=session['user_logged'], title='Cockpit do Trader',
                           title_page='Cockpit', list_assets=lista)


@app.route('/adm')
def adm():
    users_list = user_dao.to_list()
    return render_template('adm.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa', users=users_list)


@app.route('/portfolio')
def portfolio():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?proxima=portfolio')

    return render_template('portfolio.html', title='Cadastro de Ativos',
                           user_logged=session['user_logged'],
                           title_page='Portfólio')


@app.route('/portfolio-register', methods=['POST', ])
def portfolio_register():
    asset = request.form['asset']
    ticker = asset.upper() + '.SA'
    b3 = yf.download(ticker, period='1mo', auto_adjust=True)
    print(b3['Close'])
    return redirect(url_for('index'))


@app.route('/register')
def register_user():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?proxima=register')
    return render_template('registerUser.html', title_page='Cadastro de usuário', title='Cadastro')


@app.route('/update-user/<int:id_user>')
def update_user(id_user):
    user_edit = user_dao.searh_for_id(id_user)
    name_image = recovery_image(id_user)
    print(name_image)

    return render_template('updateUser.html',
                           title='Editar',
                           title_page='Editar usuário',
                           user=user_edit,
                           image_profile=name_image)


@app.route('/delete-user/<int:id_user>')
def delete_user(id_user):
    user_dao.to_delete(id_user)
    return redirect(url_for('index'))


@app.route('/register-update-user/<int:id_user>', methods=['POST'])
def register_update_user(id_user):
    user_init = user_dao.searh_for_id(id_user)
    user_name = request.form['name']
    user_email = request.form['email']
    user_cell = request.form['cell']
    user_hash = user_init.hash
    new_user = User(user_name, user_email, user_cell, user_hash, id_user=id_user)
    user_dao.to_save(new_user)

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time()
    delete_file(new_user.id)
    file.save(f'{upload_path}/images/thumb{new_user.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/user', methods=['POST'])
def user():
    user_name = request.form['name']
    user_email = request.form['email']
    user_cell = request.form['cell']
    user_hash = request.form['hash_user']
    user_created = datetime.datetime.now()
    user_updated = user_created
    if "" in request.form.values():
        flash('VALORES INVÁLIDOS')
        return redirect(url_for('register_user'))
    new_user = User(user_name, user_email, user_cell, user_hash, user_created, user_updated)
    new_user = user_dao.to_save(new_user)

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time()
    file.save(f'{upload_path}/images/thumb{new_user.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/medias/images/<file_name>')
def image(file_name):
    return send_from_directory('medias/images', file_name)


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', title_page='Login de Usuário', title='Login', proxima=proxima)


@app.route('/auth', methods=['POST', ])
def auth():
    user_in = request.form['user']
    password_in = request.form['password']
    users_list = user_dao.to_auth(user_in, password_in)

    if users_list:
        session['user_logged'] = request.form['user']
        flash(request.form['user'] + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(f'/{proxima_pagina}')

    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))
