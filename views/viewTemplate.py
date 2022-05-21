from flask import render_template, request, session, flash, redirect, url_for
from helpers import *
from main import user_dao, app


@app.route('/')
def index():
    users_list = user_dao.to_list()
    return render_template('index.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa',
                           user_logged=verify_user_logged(),
                           users=users_list)


@app.route('/login')
def login():
    next_page = request.args.get('next-page')
    return render_template('login.html', title_page='Login de Usuário', title='Login', next=next_page)


@app.route('/auth', methods=['POST', ])
def auth():
    user_in = request.form['user']
    password_in = request.form['password']
    users_list = user_dao.to_auth(user_in, password_in)

    if users_list:
        session['user_logged'] = request.form['user']
        flash(request.form['user'] + ' logou com sucesso!', 'alert alert-success' )
        next_page = request.form['next']
        return redirect(f'/{next_page}')

    else:
        flash('Não logado, tente novamente!', 'alert alert-danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('Nenhum usuário logado!', 'alert alert-primary')
    return redirect(url_for('index'))


@app.route('/adm')
def adm():
    if 'user_logged' not in session or session['user_logged'] is None:
        return redirect('/login?next-page=adm')
    users_list = user_dao.to_list()
    return render_template('adm.html', title='Jogo da Bolsa', title_page='Jogo da Bolsa',
                           user_logged=session['user_logged'],
                           users=users_list)


@app.route('/register')
def register_user():
    return render_template('registerUser.html', title_page='Cadastro de usuário', title='Cadastro')

