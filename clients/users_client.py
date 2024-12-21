import requests


class UserClient:
    BASE_URL = "http://127.0.0.1:8081/Medifli"

    @staticmethod
    def get_user(id_user):
        url = f'{UserClient.BASE_URL}/users/{id_user} -H "Accept: application/json"'
        response = requests.get(url)
        return UserClient.handle_response(response)

    @staticmethod
    def get_profile(id_profile):
        url = f'{UserClient.BASE_URL}/profiles/{id_profile} -H "Accept: application/json"'
        response = requests.get(url)
        return UserClient.handle_response(response)

    @staticmethod
    def handle_response(response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
