class Review:
    def __init__(self, idReview, rating, commentary, idProfileUser, idContent):
        self.idReview = idReview
        self.rating = rating
        self.commentary = commentary
        self.idProfileUser = idProfileUser
        self.idContent = idContent

    def toDBCollection(self):
        return {
            'idReview': self.idReview,
            'rating': self.rating,
            'commentary': self.commentary,
            'idProfileUser': self.idProfileUser,
            'idContent': self.idContent
        }
