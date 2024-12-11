class User:
    def __init__(self, id_user, username, email):
        self.id_user = id_user
        self.username = username
        self.email = email

    def toDBCollection(self):
        return {
            'id_user': self.id_user,
            'username': self.username,
            'email': self.email
        }
