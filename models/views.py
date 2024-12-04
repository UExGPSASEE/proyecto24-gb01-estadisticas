class View:
    def __init__(self, id_view, date_init, is_finished, date_finish, id_profile, id_content, type_content):
        self.id_view = id_view
        self.date_init = date_init
        self.is_finished = is_finished
        self.date_finish = date_finish
        self.id_profile = id_profile
        self.id_content = id_content
        self.type_content = type_content

    def toDBCollection(self):
        return {
            'id_view': self.id_view,
            'date_init': self.date_init,
            'is_finished': self.is_finished,
            'date_finish': self.date_finish,
            'id_profile': self.id_profile,
            'id_content': self.id_content,
            'type_content': self.type_content
        }
