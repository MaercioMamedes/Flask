class User:
    def __init__(self, name, email, cell):
        self._name = name
        self._email = email
        self._cell = cell

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def cell(self):
        return self._cell
