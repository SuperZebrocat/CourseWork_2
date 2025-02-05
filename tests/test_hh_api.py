from unittest.mock import MagicMock, patch

import requests

from src.hh_api import HeadHunterAPI


@patch("requests.get")
def test_get_vacancies_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [{"id": 1, "name": "Vacancy 1"}, {"id": 2, "name": "Vacancy 2"}],
        "page": 1,
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    mock_response_empty = MagicMock()
    mock_response_empty.json.return_value = {"items": [], "page": 2}
    mock_get.side_effect = [mock_response, mock_response_empty]

    api = HeadHunterAPI()

    vacancies = api.get_vacancies(keyword="Python")

    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Vacancy 1"
    assert vacancies[1]["name"] == "Vacancy 2"


@patch("requests.get")
def test_get_vacancies_empty_result(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": [], "page": 0}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    api = HeadHunterAPI()

    vacancies = api.get_vacancies(keyword="InvalidKeyword")

    assert len(vacancies) == 0


@patch("requests.get")
def test_api_response_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException

    api = HeadHunterAPI()

    vacancies = api.get_vacancies(keyword="Python")

    assert len(vacancies) == 0
