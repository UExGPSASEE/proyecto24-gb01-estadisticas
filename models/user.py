class User:
    def __init__(self, idUser, username, email, password):
        self.idUser = idUser
        self.username = username
        self.email = email
        self.password = password

    def toDBCollection(self):
        return {
            'idUser': self.idUser,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
