class View:
    def __init__(self, idView, dateInit, dateFinish, idContent, idProfile):
        self.idView = idView
        self.dateInit = dateInit
        self.dateFinish = dateFinish
        self.idContentd = idContent
        self.idProfile = idProfile

    def toDBCollection(self):
        return{
            'idView' : self.idView,
            'dateInit' : self.dateInit,
            'dateFinish' : self.dateFinish,
            'idContent' : self.idContent,
            'idProfile' : self.idProfile
        }