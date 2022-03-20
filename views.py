from dao import *
from main import db, app
from time import time
from helpers import *


portfolio_dao = PortfolioDao(db)
user_dao = UserDao(db)


@app.route('/')
def index():
    users_list = user_dao.to_list()
    return render_template('index.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa', users=users_list)


@app.route('/adm')
def adm():
    users_list = user_dao.to_list()
    return render_template('adm.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa', users=users_list)


@app.route('/portfolio')
def portfolio():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?proxima=portfolio')
    return render_template('portfolio.html', title='Cadastro de Ativos', title_page='Portfólio')


@app.route('/portfolio-register', methods=['POST', ])
def portfolio_register():
    print('salvou')
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
    timestamp = time.time()
    delete_file(new_user.id)
    file.save(f'{upload_path}/images/thumb{new_user.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/user', methods=['POST'])
def user():
    user_name = request.form['name']
    user_email = request.form['email']
    user_cell = request.form['cell']
    user_hash = request.form['hash_user']
    new_user = User(user_name, user_email, user_cell, user_hash)
    new_user = user_dao.to_save(new_user)

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
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