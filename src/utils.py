import re

from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy


def get_vacancies_from_api(keyword: str = None) -> list[dict]:
    """Функция для получения списка вакансий по ключевому слову от API"""
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(keyword)
    return hh_vacancies


def filter_vacancies(vacancies: list[dict], filter_words: list) -> list[dict]:
    """Функция для фильтрации списка вакансий по пользовательскому запросу"""
    filter_words_list = [word.lower() for word in filter_words]
    filtered_vacancies = []
    for vacancy in vacancies:
        if any(word in str(value).lower() for value in vacancy.values() for word in filter_words_list):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def filter_vacancies_by_salary(vacancies: list[dict], salary_range: str) -> list[Vacancy]:
    """Функция для фильтрации вакансий, подходящих под заданный диапазон зарплат"""
    patterns = re.compile(r"\d[\d\s]*")  # получаем диапазон зарплат из пользовательского ввода
    salary_range_numbers = re.findall(patterns, salary_range)
    salary_range_int_list = sorted([int(i.replace(" ", "")) for i in salary_range_numbers])
    if len(salary_range_int_list) == 2:
        min_range, max_range = salary_range_int_list
    else:
        return []

    ranged_vacancies_by_salary = []
    if min_range and max_range:
        vacancies_obj_list = Vacancy.cast_to_object_list(vacancies)

        for vacancy in vacancies_obj_list:
            salary_from = Vacancy.get_min_salary(vacancy.salary)
            salary_to = Vacancy.get_max_salary(vacancy.salary)

            if salary_from > 0 and salary_to > 0:
                if (
                    min_range <= salary_from <= max_range
                    or min_range <= salary_to <= max_range
                    or (salary_from <= min_range and salary_to >= max_range)
                ):
                    ranged_vacancies_by_salary.append(vacancy)
            elif salary_from == salary_to:
                if min_range <= salary_from <= max_range:
                    ranged_vacancies_by_salary.append(vacancy)

    return ranged_vacancies_by_salary


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """Функция для сортировки вакансий по сумме зарплаты в порядке возрастания"""
    sorted_vacancies = sorted(vacancies)
    return sorted_vacancies


def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """Функция для получения топ-n зарплат по запросу пользователя"""
    return vacancies[:top_n]


def print_vacancies(vacancies: list[Vacancy]) -> None:
    """Функция для отображения информации по отфильтрованным и отсортированным вакансиям"""
    print(f"По вашему запросу найдено {len(vacancies)} вакансий:")
    for index, vacancy in enumerate(vacancies, start=1):
        print(
            f"{index}. Название вакансии: {vacancy.name}\nЗаработная плата: {vacancy.salary} руб.\n"
            f"Требования к соискателю: {vacancy.requirement}\nСсылка на вакансию: {vacancy.url}\n"
        )
