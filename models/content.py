from enum import Enum


class ContentType(Enum):
    MOVIE = 1
    SERIES = 2
    SEASON = 3
    CATEGORY = 4


class Content:
    def __init__(self, idContent, title, urlVideo, duration, contentType):
        self.idContent = idContent
        self.title = title
        self.urlVideo = urlVideo
        self.duration = duration
        self.contentType = contentType

    def getContentType(self):
        return self.contentType


def getContentTypeStr(contentType: ContentType):
    switch = {
        ContentType.MOVIE: 'movie',
        ContentType.SERIES: 'series',
        ContentType.SEASON: 'season',
        ContentType.CATEGORY: 'category'
    }
    return switch.get(contentType, 'other')


def getContentType(contentTypeStr: str):
    switch = {
        'movie': ContentType.MOVIE,
        'series': ContentType.SERIES,
        'season': ContentType.SEASON,
        'category': ContentType.CATEGORY
    }
    return switch.get(contentTypeStr, 'other')
