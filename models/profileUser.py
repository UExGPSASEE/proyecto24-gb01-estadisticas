class ProfileUser:
    def __init__(self, id_profile, name, id_user, id_language):
        self.id_profile = id_profile
        self.name = name,
        self.id_user = id_user,
        self.id_language = id_language

    def toDBCollection(self):
        return {
            'id_profile': self.id_profile,
            'name': self.name,
            'id_user': self.id_user,
            'id_language': self.id_language
        }
