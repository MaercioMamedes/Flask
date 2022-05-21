import datetime
from time import time

from flask import render_template, request, session, flash, redirect, url_for, send_from_directory
from helpers import *
from model.models import *
from main import user_dao


@app.route('/update-user/<int:id_user>')
def update_user(id_user):
    user_edit = user_dao.searh_for_id(id_user)
    name_image = recovery_image(id_user)

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