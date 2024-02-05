import io
from typing import BinaryIO

import requests
import tempfile


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
                print(response.status_code, response.json())
                return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def upload_file(file: BinaryIO, token: str, path:str) -> None or dict:
        if file is None:
            raise ValueError("File is required - Param file is None")
        if token is None:
            raise ValueError("Token is required")
        if path is None:
            raise ValueError("Path is required")

        url = f"{TempLinkShareAPI.URL_BASE}/file/upload"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            file_content = io.BytesIO(file.read())
            format_file = path.split("/")[-1].split(".")[-1]

            if format_file:
                format_file = "." + format_file

            with tempfile.NamedTemporaryFile(delete=False, suffix=format_file) as temp:
                print(temp.name)
                temp.write(file_content.read())

                response = requests.post(url, headers=headers,
                                         files={"file": (temp.name, open(temp.name, "rb"),
                                                         "multipart/form-data")})
                if response.status_code == 201:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception("Invalid token")
                else:
                    print(response.status_code, response.json())
                    raise Exception(response.json())

        except Exception as e:
            print(e)
            raise Exception(e)

    @staticmethod
    def refresh_token(user_token: str) -> dict:
        url = f"{TempLinkShareAPI.URL_BASE}/authenticate/refresh"
        headers = {"Authorization": f"Bearer {user_token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(response)
                return response.json()
            else:
                print(response.status_code, response.json())
                raise Exception(response.json())
        except Exception as e:
            print(e)
            raise Exception(e)
