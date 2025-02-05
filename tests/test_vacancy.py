import pytest

from src.vacancy import Vacancy


def test_vacancy_init(test_vacancy1):
    assert test_vacancy1.name == "Python Developer"
    assert test_vacancy1.vacancy_id == "123456"
    assert test_vacancy1.url == "<https://hh.ru/vacancy/123456>"
    assert test_vacancy1.salary == "100000-150000"
    assert test_vacancy1.requirement == "Требования: опыт работы от 3 лет..."


def test_invalid_init(test_vacancy1):
    with pytest.raises(AttributeError):
        test_vacancy1.invalid_attribute = "test"


def test_validate_salary_none():
    vacancy = Vacancy(salary=None)
    assert vacancy.salary == "0"


def test_validate_salary():
    vacancy = Vacancy(salary="150 000")
    assert vacancy.salary == "150000"


def test_get_vacancy_id(test_vacancy1):
    assert test_vacancy1.get_vacancy_id() == "123456"


def test_cast_to_object_list(test_vacancies_from_api):
    Vacancy.current_vacancies.clear()
    vacancies_object_list = Vacancy.cast_to_object_list(test_vacancies_from_api)

    assert len(vacancies_object_list) == 2

    assert vacancies_object_list[0].name == "Backend разработчик Python"
    assert vacancies_object_list[0].vacancy_id == "115914636"
    assert vacancies_object_list[0].url == "https://hh.ru/vacancy/115914636"
    assert vacancies_object_list[0].salary == "100000"
    assert vacancies_object_list[0].requirement == "Техническое образование."

    assert vacancies_object_list[1].name == "Разработчик Python"
    assert vacancies_object_list[1].vacancy_id == "115914600"
    assert vacancies_object_list[1].url == "https://hh.ru/vacancy/115914600"
    assert vacancies_object_list[1].salary == "150000"
    assert vacancies_object_list[1].requirement == "Опыт работы от 3х лет"


def test_from_object_to_dict(test_vacancy1):
    vacancy_dict = Vacancy.from_object_to_dict(test_vacancy1)
    assert vacancy_dict == {
        "name": "Python Developer",
        "vacancy_id": "123456",
        "url": "<https://hh.ru/vacancy/123456>",
        "salary": "100000-150000 руб.",
        "requirement": "Требования: опыт работы от 3 лет...",
    }


def test_parse_salary_int():
    salary = 50000
    parsed_salary = Vacancy.parse_salary(salary)

    assert parsed_salary == 50000


def test_parse_salary_str():
    salary = "50 000 руб."
    parsed_salary = Vacancy.parse_salary(salary)

    assert parsed_salary == 50000


def test_parse_salary_invalid():
    salary = "руб."
    parsed_salary = Vacancy.parse_salary(salary)

    assert parsed_salary == 0


def test_get_min_salary_if_range():
    salary_str = "100 000 - 150000"
    min_salary = Vacancy.get_min_salary(salary_str)

    assert min_salary == 100000


def test_get_min_salary_if_not_range():
    salary_str = "100 000"
    min_salary = Vacancy.get_min_salary(salary_str)

    assert min_salary == 100000


def test_get_max_salary_if_range():
    salary_str = "100 000 - 150000"
    min_salary = Vacancy.get_max_salary(salary_str)

    assert min_salary == 150000


def test_get_max_salary_if_not_range():
    salary_str = "150 000"
    min_salary = Vacancy.get_max_salary(salary_str)

    assert min_salary == 150000


def test_lt_true(test_vacancy1, test_vacancy2):
    result = Vacancy.__lt__(test_vacancy1, test_vacancy2)

    assert result is True


def test_lt_false(test_vacancy2, test_vacancy3):
    result = Vacancy.__lt__(test_vacancy2, test_vacancy3)

    assert result is False
