class View:
    def __init__(self, idView, dateInit, isFinished, dateFinish, idContent, idProfile):
        self.idView = idView
        self.dateInit = dateInit
        self.isFinished = isFinished
        self.dateFinish = dateFinish
        self.idContent = idContent
        self.idProfile = idProfile

    def toDBCollection(self):
        return{
            'idView' : self.idView,
            'dateInit' : self.dateInit,
            'isFinished' : self.isFinished,
            'dateFinish' : self.dateFinish,
            'idContent' : self.idContent,
            'idProfile' : self.idProfile
        }