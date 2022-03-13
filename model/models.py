# Modelos do Sistemas


class User:
    def __init__(self, name, email, cell, hash_user, id_user=None):
        self._id = id_user
        self._name = name
        self._email = email
        self._cell = cell
        self._hash = hash_user

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def cell(self):
        return self._cell

    @property
    def hash(self):
        return self._hash

    @id.setter
    def id(self, id_user):
        self._id = id_user

    @name.setter
    def name(self, name):
        self._name = name

    @email.setter
    def email(self, email):
        self._email = email

    @cell.setter
    def cell(self, cell):
        self._cell = cell


class Portfolio:
    def __init__(self, fk_user, portfolio_name, id_portfolio=None):
        self._id = id_portfolio
        self._fk_user = fk_user
        self._name = portfolio_name

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @name.setter
    def name(self, name):
        self._name = name
