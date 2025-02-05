import requests

from .base_classes import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс для работы с сервисом hh.ru"""

    url: str
    headers: dict
    params: dict
    vacancies: list

    def __init__(self):
        """Метод инициализации экземпляра класса"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100, "only_with_salary": True}
        self.__vacancies = []

    def _api_response(self):
        """Метод подключения к API HeadHunter"""
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_vacancies(self, keyword=None):
        """Метод для загрузки данных о вакансиях с hh.ru по ключевому слову"""
        if keyword:
            self.__params["text"] = keyword
        else:
            self.__params["text"] = ""
        self.__params["page"] = 0  # Сбрасываем страницу перед загрузкой
        self.__vacancies = []  # Сбрасываем список вакансий перед загрузкой
        while self.__params.get("page") != 20:
            response_from_api = self._api_response()
            if response_from_api is None:
                break
            vacancies = response_from_api.get("items")
            if vacancies:
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
            else:
                break

        return self.__vacancies
