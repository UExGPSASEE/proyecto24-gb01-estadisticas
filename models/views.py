class View:
    def __init__(self, idView, dateInit, isFinished, dateFinish, idProfile, idContent, typeContent):
        self.idView = idView
        self.dateInit = dateInit
        self.isFinished = isFinished
        self.dateFinish = dateFinish
        self.idProfile = idProfile
        self.idContent = idContent
        self.typeContent = typeContent

    def toDBCollection(self):
        return {
            'idView': self.idView,
            'dateInit': self.dateInit,
            'isFinished': self.isFinished,
            'dateFinish': self.dateFinish,
            'idProfile': self.idProfile,
            'idContent': self.idContent,
            'typeContent': self.typeContent
        }
