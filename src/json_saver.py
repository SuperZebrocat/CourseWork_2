import json
import os
from collections import defaultdict

from src.base_classes import BaseJSONSaver
from src.vacancy import Vacancy

CURRENT_DIR = os.path.dirname(__file__)
PATH_FILE_JSON = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data", "vacancies.json"))


class JSONSaver(BaseJSONSaver):
    """Класс для работы с JSON-файлами"""

    file_path: str

    def __init__(self, file_path=None):
        """Метод инициализации экземпляра класса"""
        if file_path is None:
            self.__file_path = PATH_FILE_JSON
        else:
            self.__file_path = file_path

    def read_data_json(self):
        """Метод получения данных о вакансиях из JSON-файла"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                read_data = json.load(json_file)
            return read_data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        except Exception:
            return []

    def write_to_file(self, data_to_write):
        """Метод записи данных о вакансиях в JSON-файл"""
        try:
            with open(self.__file_path, "w", encoding="utf-8") as json_file:
                json.dump(data_to_write, json_file, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"Ошибка ввода-вывода: {e}")
        except TypeError as e:
            print(f"Ошибка сериализации данных: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    @staticmethod
    def convert_vacancy_to_dict_list(vacancy):
        """Метод для проверки принадлежности вакансий к классу Vacancy и создание из них списка словарей"""
        if isinstance(vacancy, Vacancy):
            return [vacancy.from_object_to_dict()]
        elif isinstance(vacancy, list) and all(isinstance(v, Vacancy) for v in vacancy):
            return [v.from_object_to_dict() for v in vacancy]
        return []

    def add_vacancy(self, vacancy):
        """Метод добавления данных о новых вакансиях"""
        vacancy_dict_list = self.convert_vacancy_to_dict_list(vacancy)
        if vacancy_dict_list:
            read_data = self.read_data_json()
            unique_vacancies = defaultdict(dict)
            for vacancy in read_data:
                unique_vacancies[vacancy["vacancy_id"]] = vacancy
            for vacancy in vacancy_dict_list:
                unique_vacancies[vacancy["vacancy_id"]] = vacancy
            data_to_write = list(unique_vacancies.values())
            self.write_to_file(data_to_write)
        else:
            print("Нет данных для записи")

    def delete_vacancy(self, vacancy):
        """Метод удаления данных о вакансиях"""
        vacancy_dict_list = self.convert_vacancy_to_dict_list(vacancy)
        if vacancy_dict_list:
            read_data = self.read_data_json()
            id_list_to_remove = {vacancy["vacancy_id"] for vacancy in vacancy_dict_list}
            data_to_write = [vacancy for vacancy in read_data if vacancy["vacancy_id"] not in id_list_to_remove]
            self.write_to_file(data_to_write)
