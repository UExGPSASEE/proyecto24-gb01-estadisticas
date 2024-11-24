import requests


class UserClient:
    BASE_URL = "http://127.0.0.1:8081/Medifli"

    @staticmethod
    def getUser(idUser):
        url = f'{UserClient.BASE_URL}/users/{idUser} -H "Accept: application/json"'
        response = requests.get(url)
        return UserClient.handleResponse(response)

    @staticmethod
    def getProfile(idProfile):
        url = f'{UserClient.BASE_URL}/profiles/{idProfile} -H "Accept: application/json"'
        response = requests.get(url)
        return UserClient.handleResponse(response)

    @staticmethod
    def handleResponse(response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
