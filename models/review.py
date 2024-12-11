class Review:
    def __init__(self, id_review, rating, commentary, id_profile, id_content, type_content):
        self.id_review = id_review
        self.rating = rating
        self.commentary = commentary
        self.id_profile = id_profile
        self.id_content = id_content
        self.type_content = type_content

    def toDBCollection(self):
        return {
            'id_review': self.id_review,
            'rating': self.rating,
            'commentary': self.commentary,
            'id_profile': self.id_profile,
            'id_content': self.id_content,
            'type_content': self.type_content
        }
