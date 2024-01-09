import io
import re

from bs4 import BeautifulSoup
from requests import Session

from services import ServiceAnswer
from services.services_implementation.base_service import BaseService
from utils import Singleton


class Informatics(metaclass=Singleton):
    __session: Session
    __cookies: {}
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.__session = Session()
        self.username = username
        self.password = password

    def auth(self) -> None:
        headers = {"User-Agent": "insomnia/8.3.0"}
        res = self.__session.get("https://informatics.msk.ru/login/index.php", headers=headers)
        logintoken = BeautifulSoup(res.text, "html.parser").find('input', {'name': 'logintoken', "type": "hidden"})[
            "value"]

        data = {
            "anchor": "",
            "username": self.username,
            "password": self.password,
            "logintoken": logintoken
        }

        self.__session.post("https://informatics.msk.ru/login/index.php", data=data, headers=headers)

    def send(self, url: str, file: io.BytesIO) -> None:
        headers = {
          "User-Agent": "insomnia/8.3.0",
        }
        files = {'file': file, "lang_id": (None, 3),}
        self.__session.get(url, headers=headers)
        req = self.__session.post(f"https://informatics.msk.ru/py/problem/{self.__get_task_id(url)}/submit",
                                  files=files,
                                  headers=headers)
        print(req.text)

    def get_result(self, run_id: int):
        headers = {
            "User-Agent": "insomnia/8.3.0",
        }
        res = self.__session.get(f"https://informatics.msk.ru/py/protocol/get/{run_id}", headers=headers)
        print(res.text)

    def __get_task_id(self, url: str) -> int:
        res = self.__session.get(url, headers={"User-Agent": "insomnia/8.3.0"})
        id = int(re.findall(r"\d+", re.findall(r"view\.php\?id=\d+&submit", res.text)[0])[0])
        return id


class InformaticsService(BaseService):
    netloc = "informatics.msk.ru"

    def __get_informatics_instance(self) -> Informatics:
        username, password = self._get_single_data()
        informatics = Informatics(username, password)
        if not (informatics.username == username and informatics.password == password):
            informatics.username = username
            informatics.password = password
        return informatics

    async def submit(self, url: str, file: io.BytesIO) -> ServiceAnswer:
        informatics = self.__get_informatics_instance()
        result = informatics.send(url, file)

