class Review:
    def __init__(self, idReview, rating, commentary, idProfile, idContent):
        self.idReview = idReview
        self.rating = rating
        self.commentary = commentary
        self.idProfile = idProfile
        self.idContent = idContent

    def toDBCollection(self):
        return {
            'idReview': self.idReview,
            'rating': self.rating,
            'commentary': self.commentary,
            'idProfile': self.idProfile,
            'idContent': self.idContent
        }
