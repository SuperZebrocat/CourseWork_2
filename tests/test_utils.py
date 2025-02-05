import sys
from io import StringIO
from unittest.mock import patch

from src.utils import (filter_vacancies, filter_vacancies_by_salary, get_top_vacancies, get_vacancies_from_api,
                       print_vacancies, sort_vacancies)


@patch("src.hh_api.HeadHunterAPI.get_vacancies")
def test_get_vacancies_from_api_success(mock_get_vacancies):
    mock_get_vacancies.return_value = [{"id": 1, "name": "Vacancy 1"}, {"id": 2, "name": "Vacancy 2"}]
    result = get_vacancies_from_api(keyword="developer")
    expected_result = [{"id": 1, "name": "Vacancy 1"}, {"id": 2, "name": "Vacancy 2"}]
    assert result == expected_result

    mock_get_vacancies.assert_called_once_with("developer")


@patch("src.hh_api.HeadHunterAPI.get_vacancies")
def test_get_vacancies_from_api_empty(mock_get_vacancies):
    mock_get_vacancies.return_value = []
    result = get_vacancies_from_api(keyword="developer")
    expected_result = []
    assert result == expected_result

    mock_get_vacancies.assert_called_once_with("developer")


def test_filter_vacancies_success(test_vacancies_from_api, test_filtered_vacancies):
    filter_words = ["Техническое", "образование"]
    filtered_vacancies = filter_vacancies(test_vacancies_from_api, filter_words)

    assert filtered_vacancies == test_filtered_vacancies


def test_filter_vacancies_empty_list(test_vacancies_from_api):
    filter_words = ["Свободный", "график"]
    filtered_vacancies = filter_vacancies(test_vacancies_from_api, filter_words)

    assert filtered_vacancies == []


def test_filter_vacancies_by_salary(test_vacancies_salary):
    salary_range = "50000 - 100000"
    filtered_vacancies = filter_vacancies_by_salary(test_vacancies_salary, salary_range)

    assert len(filtered_vacancies) == 4

    assert filtered_vacancies[0].name == "Вакансия1"
    assert filtered_vacancies[0].salary == "70000"

    assert filtered_vacancies[1].name == "Вакансия2"
    assert filtered_vacancies[1].salary == "70000"

    assert filtered_vacancies[2].name == "Вакансия3"
    assert filtered_vacancies[2].salary == "70000"

    assert filtered_vacancies[3].name == "Вакансия4"
    assert filtered_vacancies[3].salary == "20000-120000"


def test_filter_vacancies_by_salary_invalid_range1(test_vacancies_salary):
    salary_range = "50000"

    assert filter_vacancies_by_salary(test_vacancies_salary, salary_range) == []


def test_filter_vacancies_by_salary_invalid_range2(test_vacancies_salary):
    salary_range = "invalid_range"

    assert filter_vacancies_by_salary(test_vacancies_salary, salary_range) == []


def test_sort_vacancies(test_vacancy1, test_vacancy2, test_vacancy3):
    vacancies = [test_vacancy1, test_vacancy2, test_vacancy3]

    sorted_vacancies = sort_vacancies(vacancies)

    assert sorted_vacancies[0].salary == "50000"
    assert sorted_vacancies[1].salary == "100000-150000"
    assert sorted_vacancies[2].salary == "200000"


def test_get_top_vacancies(test_vacancy1, test_vacancy2, test_vacancy3):
    vacancies = [test_vacancy1, test_vacancy2, test_vacancy3]

    top_vacancies = get_top_vacancies(vacancies, 2)

    assert len(top_vacancies) == 2


def test_print_vacancies(test_vacancy1, test_vacancy2, test_vacancy3):
    vacancies = [test_vacancy1, test_vacancy2]

    captured_output = StringIO()
    sys.stdout = captured_output

    print_vacancies(vacancies)

    sys.stdout = sys.__stdout__

    expected_output = (
        "По вашему запросу найдено 2 вакансий:\n"
        "1. Название вакансии: Python Developer\n"
        "Заработная плата: 100000-150000 руб.\n"
        "Требования к соискателю: Требования: опыт работы от 3 лет...\n"
        "Ссылка на вакансию: <https://hh.ru/vacancy/123456>\n\n"
        "2. Название вакансии: Python Developer Middle\n"
        "Заработная плата: 200000 руб.\n"
        "Требования к соискателю: Требования: опыт работы от 3 лет...\n"
        "Ссылка на вакансию: <https://hh.ru/vacancy/123400>\n\n"
    )

    assert captured_output.getvalue() == expected_output
