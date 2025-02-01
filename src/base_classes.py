from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный метод для работы с API"""

    @abstractmethod
    def _api_response(self):
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        """Метод получения вакансий от API"""
        pass


class BaseJSONSaver(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def read_data_json(self):
        """Метод чтения JSON-файла и получения данных из файла"""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Метод добавления данных о вакансиях в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """Метод удаления данных о вакансиях из файла"""
        pass
