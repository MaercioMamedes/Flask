from flask import session
import os
from main import app


def recovery_image(id_user):
    upload_path = app.config['UPLOAD_PATH']
    for name_file in os.listdir(f'{upload_path}/images'):
        if f'thumb{id_user}' in name_file:
            return name_file
    return 'image_default.jpg'


def delete_file(id_user):
    upload_path = app.config['UPLOAD_PATH']
    if recovery_image(id_user) is not None:
        file = recovery_image(id_user)
        if file == 'image_default.jpg':
            return False
        else:
            os.remove(os.path.join(f'{upload_path}/images', file))


def verify_user_logged():
    if 'user_logged' in session and session['user_logged'] is not None:
        return session['user_logged']

    else:
        return False
