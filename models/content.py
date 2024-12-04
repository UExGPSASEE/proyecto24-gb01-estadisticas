from enum import Enum


class ContentType(Enum):
    MOVIE = 1
    SERIES = 2
    SEASON = 3
    CATEGORY = 4


class Content:
    def __init__(self, id_content, title, url_video, duration, content_type):
        self.id_content = id_content
        self.title = title
        self.url_video = url_video
        self.duration = duration
        self.content_type = content_type

    def get_content_type(self):
        return self.content_type


def get_content_type_str(content_type: ContentType):
    switch = {
        ContentType.MOVIE: 'movie',
        ContentType.SERIES: 'series',
        ContentType.SEASON: 'season',
        ContentType.CATEGORY: 'category'
    }
    return switch.get(content_type, 'other')


def get_content_type(content_type_str: str):
    switch = {
        'movie': ContentType.MOVIE,
        'series': ContentType.SERIES,
        'season': ContentType.SEASON,
        'category': ContentType.CATEGORY
    }
    return switch.get(content_type_str, 'other')
