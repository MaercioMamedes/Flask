from model.models import *


def portfolio_format(list_portfolio):
    def create_game_with_tuple(tuple_object):
        return Portfolio(tuple_object[1], tuple_object[2], id_portfolio=tuple_object[0])

    return list(map(create_game_with_tuple, list_portfolio))


def user_list_format(list_user):

    def create_user_with_tuple(tuple_object):
        return User(tuple_object[1], tuple_object[2], tuple_object[3], tuple_object[4], tuple_object[5],
                    tuple_object[6], id_user=tuple_object[0])

    return list(map(create_user_with_tuple, list_user))


def users_format(tuple_object):
    return User(tuple_object[1], tuple_object[2], tuple_object[3], tuple_object[4], tuple_object[5],
                tuple_object[6], id_user=tuple_object[0])


class PortfolioDao:

    def __init__(self, data_base):
        self.__db = data_base
        self.__SQL_CREATE_PORTFOLIO = 'INSERT INTO `GameDataBase`.`Portfolio` (`fk_user`, `name`) VALUES (%d, %s)'
        self.__SQL_LIST_PORTFOLIO = 'SELECT * from `GameDataBase`.`Portfolio`'
        self.__SQL_SEARCH_FOR_ID = 'SELECT * from `GameDataBase`.`Portfolio` WHERE id = %d'
        self.__SQL_DELETE_PORTFOLIO = 'DELETE from `GameDataBase.`Portfolio` where id = %d'
        self.__SQL_UPDATE_PORTFOLIO = 'UPDATE `GameDataBase`.`Portfolio` SET `name` = %s WHERE (`id` = %d)'

    def to_save(self, portifolio):
        cursor = self.__db.connection.cursor()
        if portifolio.id:
            cursor.execute(self.__SQL_UPDATE_PORTFOLIO, (portifolio.name, portifolio.id))
        else:
            cursor.execute(self.__SQL_CREATE_PORTFOLIO, (portifolio.fk_user, portifolio.name))
            portifolio.id = cursor.lastrowid
        self.__db.connection.commit()
        return portifolio

    def to_list(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(self.__SQL_LIST_PORTFOLIO)
        list_portifolio = portfolio_format(cursor.fetchall())
        return list_portifolio

    def search_for_id(self, portifolio_id):
        cursor = self.__db.connection.cursor()
        cursor.execute(self.__SQL_SEARCH_FOR_ID, (portifolio_id,))
        tuple_object = cursor.fetchone()
        return Portfolio(tuple_object[1], tuple_object[2], id_portfolio=tuple_object[0])

    def to_delete(self, portfolio_id):
        self.__db.connection.cursor().execute(self.__SQL_DELETE_PORTFOLIO, (portfolio_id,))
        self.__db.connection.commit()


class UserDao:

    def __init__(self, data_base):
        self.__db = data_base
        self.__SQL_CREATE_USER = """INSERT INTO `GameDataBase`.
                                `User` (`name`, `email`, `cell`, `hash`, `created`,`updated`)                           
                                 VALUES (%s, %s, %s, %s, %s, %s)"""

        self.__SQL_UPDATE_USER = """UPDATE `GameDataBase`.`User` SET `name` = %s, `email` = %s, `cell` = %s, `hash` = %s 
                                    WHERE (`id` = %s)"""
        self.__SQL_USER_FOR_ID = 'SELECT * from `GameDataBase`.`User` where id = %s'
        self.__SQL_USER_AUTH = 'SELECT * from `GameDataBase`.`User` where name = %s and hash = %s'
        self.__SQL_DELETE_USER = 'DELETE FROM `GameDataBase`.`User` WHERE (`id` = %s)'
        self.__SQL_LIST_USER = 'SELECT * from `GameDataBase`.`User`'

    def searh_for_id(self, user_id):
        cursor = self.__db.connection.cursor()
        cursor.execute(self.__SQL_USER_FOR_ID, (user_id,))
        data = cursor.fetchone()
        user_db = users_format(data) if data else None
        return user_db

    def to_save(self, user):
        cursor = self.__db.connection.cursor()
        if user.id:
            cursor.execute(self.__SQL_UPDATE_USER, (user.name, user.email, user.cell,
                                                    user.hash, user.created, user.updated, user.id))
        else:
            cursor.execute(self.__SQL_CREATE_USER, (user.name, user.email, user.cell,
                                                    user.hash, user.created, user.updated))
            user.id = cursor.lastrowid
        self.__db.connection.commit()
        return user

    def to_list(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(self.__SQL_LIST_USER)
        list_users = user_list_format(cursor.fetchall())
        return list_users

    def to_auth(self, user, password):
        cursor = self.__db.connection.cursor()
        cursor.execute(self.__SQL_USER_AUTH, (user, password))
        user = users_format(cursor.fetchone())
        return user

    def to_delete(self, id_user):
        self.__db.connection.cursor().execute(self.__SQL_DELETE_USER, (id_user,))
        self.__db.connection.commit()
