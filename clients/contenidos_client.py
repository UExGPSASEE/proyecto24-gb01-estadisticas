import requests


class ContenidosClient:
    BASE_URL = "http://127.0.0.1:8082"

    @staticmethod
    def getMovie(idMovie):
        url = f"{ContenidosClient.BASE_URL}/movies/{idMovie}"
        response = requests.get(url)
        return ContenidosClient.handleResponse(response)

    @staticmethod
    def getCategory(idCategory):
        url = f"{ContenidosClient.BASE_URL}/categories/{idCategory}"
        response = requests.get(url)
        return ContenidosClient.handleResponse(response)

    @staticmethod
    def getSeries(idSeries):
        url = f"{ContenidosClient.BASE_URL}/series/{idSeries}"
        response = requests.get(url)
        return ContenidosClient.handleResponse(response)

    @staticmethod
    def getSeason(idSeason):
        url = f"{ContenidosClient.BASE_URL}/series/{idSeason}"
        response = requests.get(url)
        return ContenidosClient.handleResponse(response)

    @staticmethod
    def handleResponse(response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    @staticmethod
    def checkContentExists(idContent: int, contentType):
        found = False

        if contentType == 1:
            url = f"{ContenidosClient.BASE_URL}/movies/{idContent}"
        elif contentType == 2:
            url = f"{ContenidosClient.BASE_URL}/series/{idContent}"
        elif contentType == 3:
            url = f"{ContenidosClient.BASE_URL}/series/{idContent}"
        elif contentType == 4:
            url = f"{ContenidosClient.BASE_URL}/categories/{idContent}"
        else:
            return False

        response = requests.get(url)
        if response.status_code == 200:
            found = True

        return found
