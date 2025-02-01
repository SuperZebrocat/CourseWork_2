import io
import sys
from unittest.mock import patch

from main import user_interaction


@patch("main.get_vacancies_from_api")
@patch("sys.stdout", new_callable=io.StringIO)
@patch("builtins.input", side_effect=["Python", "3", "Техническое образование", "50000 - 100000"])
def test_main_success(mock_input, mock_stdout, mock_get_vacancies, test_main_vacancies):
    mock_get_vacancies.return_value = test_main_vacancies

    user_interaction()

    output = mock_stdout.getvalue()

    expected_output = (
        "По вашему запросу найдено 3 вакансий:\n"
        "1. Название вакансии: Backend разработчик Python\n"
        "Заработная плата: 40000-120000 руб.\n"
        "Требования к соискателю: Техническое образование\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/3\n\n"
        "2. Название вакансии: Backend разработчик Python\n"
        "Заработная плата: 50000-80000 руб.\n"
        "Требования к соискателю: Высшее образование\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/5\n\n"
        "3. Название вакансии: Backend разработчик Python\n"
        "Заработная плата: 100000 руб.\n"
        "Требования к соискателю: Техническое образование\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/1\n\n"
    )

    assert output == expected_output

    mock_get_vacancies.assert_called_once_with("Python")

    pass
