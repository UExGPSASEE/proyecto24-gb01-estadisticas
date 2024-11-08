class Review:
    def __init__(self, content_id, valoracion, comentario, profile):
        self.content_id = content_id
        self.valoracion = valoracion
        self.comentario = comentario
        self.profile = profile

    def toDBCollection(self):
        return{
            'Content_id' : self.content_id,
            'Valoracion' : self.valoracion,
            'Comentario' : self.comentario,
            'Profile' : self.profile
        }