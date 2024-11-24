class ProfileUser:
    def __init__(self, idProfile, name, idUser, idLanguage):
        self.idProfile = idProfile
        self.name = name,
        self.idUser = idUser,
        self.idLanguage = idLanguage

    def toDBCollection(self):
        return {
            'idProfile': self.idProfile,
            'name': self.name,
            'idUser': self.idUser,
            'idLanguage': self.idLanguage
        }
