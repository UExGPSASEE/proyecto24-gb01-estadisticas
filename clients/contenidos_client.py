import requests


class ContenidosClient:
    BASE_URL = "http://127.0.0.1:8082"

    @staticmethod
    def get_movie(id_movie):
        url = f"{ContenidosClient.BASE_URL}/movies/{id_movie}"
        response = requests.get(url)
        return ContenidosClient.handle_response(response)

    @staticmethod
    def get_category(id_category):
        url = f"{ContenidosClient.BASE_URL}/categories/{id_category}"
        response = requests.get(url)
        return ContenidosClient.handle_response(response)

    @staticmethod
    def get_series(id_series):
        url = f"{ContenidosClient.BASE_URL}/series/{id_series}"
        response = requests.get(url)
        return ContenidosClient.handle_response(response)

    @staticmethod
    def get_season(id_season):
        url = f"{ContenidosClient.BASE_URL}/seasons/{id_season}"
        response = requests.get(url)
        return ContenidosClient.handle_response(response)

    @staticmethod
    def handle_response(response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    @staticmethod
    def check_content_exists(id_content: int, content_type):
        found = False

        if content_type == 1:
            url = f"{ContenidosClient.BASE_URL}/movies/{id_content}"
        elif content_type == 2:
            url = f"{ContenidosClient.BASE_URL}/series/{id_content}"
        elif content_type == 3:
            url = f"{ContenidosClient.BASE_URL}/series/{id_content}"
        elif content_type == 4:
            url = f"{ContenidosClient.BASE_URL}/categories/{id_content}"
        else:
            return False

        response = requests.get(url)
        if response.status_code == 200:
            found = True

        return found
