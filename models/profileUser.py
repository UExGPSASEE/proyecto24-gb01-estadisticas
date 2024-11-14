class ProfileUser:
    def __init__(self, idProfileUser, name, pin, idUser, idLanguage):
        self.idProfileUser = idProfileUser
        self.name = name,
        self.pin = pin,
        self.idUser = idUser,
        self.idLanguage = idLanguage

    def toDBCollection(self):
        return{
            'idProfileUser' : self.idProfileUser,
            'name' : self.name,
            'pin' : self.pin,
            'idUser' : self.idUser,
            'idLanguage' : self.idLanguage
        }