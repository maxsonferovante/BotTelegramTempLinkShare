import requests


class TempLinkShareAPI:
    URL_BASE = "http://localhost:3000"

    @staticmethod
    def user_register(email: str, password: str, name: str) -> bool:
        url = f"{TempLinkShareAPI.URL_BASE}/user/register"
        payload = {
            "name": name,
            "email": email,
            "password": password
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def user_login(email: str, password: str) -> bool or str:
        url = f"{TempLinkShareAPI.URL_BASE}/authenticate/login"
        payload = {
            "email": email,
            "password": password
        }
        try:
            response = requests.request("POST", url, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return False
        except Exception as e:
            print(e)
            return False
