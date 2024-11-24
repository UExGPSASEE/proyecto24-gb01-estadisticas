class Review:
    def __init__(self, idReview, rating, commentary, idProfile, idContent, typeContent):
        self.idReview = idReview
        self.rating = rating
        self.commentary = commentary
        self.idProfile = idProfile
        self.idContent = idContent
        self.typeContent = typeContent

    def toDBCollection(self):
        return {
            'idReview': self.idReview,
            'rating': self.rating,
            'commentary': self.commentary,
            'idProfile': self.idProfile,
            'idContent': self.idContent,
            'typeContent': self.typeContent
        }
