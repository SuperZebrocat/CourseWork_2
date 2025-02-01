import json

import pytest

from src.vacancy import Vacancy


@pytest.fixture
def test_vacancy1():
    return Vacancy(
        "Python Developer",
        "<https://hh.ru/vacancy/123456>",
        "100 000-150 000 руб.",
        "Требования: опыт работы от 3 лет...",
    )


@pytest.fixture
def test_vacancy2():
    return Vacancy(
        "Python Developer Middle",
        "<https://hh.ru/vacancy/123400>",
        "200 000 руб.",
        "Требования: опыт работы от 3 лет...",
    )


@pytest.fixture
def test_vacancy3():
    return Vacancy(
        "Python Developer Junior",
        "<https://hh.ru/vacancy/123401>",
        "50000 руб.",
        "Требования: опыт работы не требуется",
    )


@pytest.fixture
def test_vacancy4():
    return Vacancy(
        "Python Developer",
        "<https://hh.ru/vacancy/1234560>",
        "100 000-150 000 руб.",
        "Требования: опыт работы от 3 лет...",
    )


@pytest.fixture
def test_vacancies_from_api():
    return [
        {
            "id": "115914636",
            "name": "Backend разработчик Python",
            "salary": {"from": 100000, "to": None, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/115914636",
            "snippet": {
                "requirement": "Техническое образование.",
            },
        },
        {
            "id": "115914600",
            "name": "Разработчик Python",
            "salary": {"from": None, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/115914600",
            "snippet": {
                "requirement": "Опыт работы от 3х лет",
            },
        },
        {
            "id": "115914601",
            "name": "Backend разработчик Python",
            "salary": {"from": "non_salary", "to": "non_salary", "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/115914601",
            "snippet": {
                "requirement": "Техническое образование.",
            },
        },
    ]


@pytest.fixture
def test_json_data(test_vacancies_from_api):
    return json.dumps(test_vacancies_from_api, indent=4)


@pytest.fixture
def mock_read_dict_list():
    return [
        {
            "name": "Python Developer",
            "vacancy_id": "123456",
            "url": "<https://hh.ru/vacancy/123456>",
            "salary": "100 000-150 000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        },
        {
            "name": "Python Developer Middle",
            "vacancy_id": "123400",
            "url": "<https://hh.ru/vacancy/123400>",
            "salary": "200 000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        },
    ]


@pytest.fixture
def test_data_to_write():
    return [
        {
            "name": "Python Developer",
            "vacancy_id": "123456",
            "url": "<https://hh.ru/vacancy/123456>",
            "salary": "100 000-150 000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        },
        {
            "name": "Python Developer Middle",
            "vacancy_id": "123400",
            "url": "<https://hh.ru/vacancy/123400>",
            "salary": "200 000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        },
        {
            "name": "Python Developer Junior",
            "vacancy_id": "123401",
            "url": "<https://hh.ru/vacancy/123401>",
            "salary": "50000 руб.",
            "requirement": "Требования: опыт работы не требуется",
        },
    ]


@pytest.fixture
def test_filtered_vacancies():
    return [
        {
            "id": "115914636",
            "name": "Backend разработчик Python",
            "salary": {"from": 100000, "to": None, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/115914636",
            "snippet": {
                "requirement": "Техническое образование.",
            },
        },
        {
            "id": "115914601",
            "name": "Backend разработчик Python",
            "salary": {"from": "non_salary", "to": "non_salary", "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/115914601",
            "snippet": {
                "requirement": "Техническое образование.",
            },
        },
    ]


@pytest.fixture
def test_vacancies_salary():
    return [
        {
            "name": "Вакансия1",
            "salary": {"from": 70000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/1",
            "snippet": {"requirement": "Опыт работы от 3х лет"},
        },
        {
            "name": "Вакансия2",
            "salary": {"to": 70000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/2",
            "snippet": {"requirement": "Опыт работы от 3х лет"},
        },
        {
            "name": "Вакансия3",
            "salary": {"from": "70 000 руб.", "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/3",
            "snippet": {"requirement": "Опыт работы от 3х лет"},
        },
        {
            "name": "Вакансия4",
            "salary": {"from": 20000, "to": 120000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/4",
            "snippet": {"requirement": "Опыт работы от 3х лет"},
        },
        {
            "name": "Вакансия5",
            "salary": {"from": 20000, "to": 45000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/5",
            "snippet": {"requirement": "Опыт работы от 3х лет"},
        },
        {
            "name": "Вакансия6",
            "salary": {"from": "no_salary", "to": "no_salary", "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/5",
            "snippet": {"requirement": "Опыт работы от 3х лет"},
        },
    ]


@pytest.fixture
def test_main_vacancies():
    return [
        {
            "id": "1",
            "name": "Backend разработчик Python",
            "salary": {"from": 100000, "to": None, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/1",
            "snippet": {
                "requirement": "Техническое образование",
            },
        },
        {
            "id": "2",
            "name": "Разработчик Python",
            "salary": {"from": None, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/2",
            "snippet": {
                "requirement": "Высшее образование",
            },
        },
        {
            "id": "3",
            "name": "Backend разработчик Python",
            "salary": {"from": 40000, "to": 120000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/3",
            "snippet": {
                "requirement": "Техническое образование",
            },
        },
        {
            "id": "4",
            "name": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/4",
            "snippet": {
                "requirement": "Высшее техническое образование",
            },
        },
        {
            "id": "5",
            "name": "Backend разработчик Python",
            "salary": {"from": 50000, "to": 80000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/5",
            "snippet": {
                "requirement": "Высшее образование",
            },
        },
    ]
