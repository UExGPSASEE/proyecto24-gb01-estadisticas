class User:
    def __init__(self, idUser, username, email):
        self.idUser = idUser
        self.username = username
        self.email = email

    def toDBCollection(self):
        return {
            'idUser': self.idUser,
            'username': self.username,
            'email': self.email
        }
