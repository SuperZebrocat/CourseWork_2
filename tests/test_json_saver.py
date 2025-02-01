import io
from unittest.mock import mock_open, patch

from src.json_saver import JSONSaver


@patch("builtins.open", new_callable=mock_open)
def test_read_json_data_success(mock_file, test_vacancies_from_api, test_json_data):
    mock_file.return_value.read.return_value = test_json_data

    saver = JSONSaver(mock_file)
    data = saver.read_data_json()
    assert data == test_vacancies_from_api


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_json_data_no_file(mock_file):

    saver = JSONSaver("file_not_found.json")
    data = saver.read_data_json()

    assert data == []


@patch("builtins.open", new_callable=mock_open)
def test_read_json_data_invalid_json(mock_file):
    mock_file.return_value.read.return_value = "invalid_json_data"

    saver = JSONSaver(mock_file)
    data = saver.read_data_json()

    assert data == []


@patch("builtins.open", new_callable=mock_open)
def test_read_json_data_exception(mock_file):
    mock_file.side_effect = Exception()

    saver = JSONSaver(mock_file)
    data = saver.read_data_json()

    assert data == []


@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def test_write_to_file_success(mock_json_dump, mock_file):
    data = {"key": "value"}

    saver = JSONSaver("test.json")
    saver.write_to_file(data)

    mock_file.assert_called_once_with("test.json", "w", encoding="utf-8")

    handle = mock_file()
    mock_json_dump.assert_called_once_with(data, handle, ensure_ascii=False, indent=4)


@patch("builtins.open", new_callable=mock_open)
def test_write_to_file_os_error(mock_file):
    mock_file.side_effect = OSError("Unable to open file")
    data = {"key": "value"}

    saver = JSONSaver("test.json")

    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        saver.write_to_file(data)
        assert "Ошибка ввода-вывода: Unable to open file" in fake_out.getvalue()


@patch("builtins.open", new_callable=mock_open)
def test_write_to_file_type_error(mock_file):
    mock_file.side_effect = TypeError()
    data = "not_json"

    saver = JSONSaver("test.json")

    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        saver.write_to_file(data)
        assert "Ошибка сериализации данных:" in fake_out.getvalue()


@patch("builtins.open", new_callable=mock_open)
def test_write_to_file_exception(mock_file):
    mock_file.side_effect = Exception()
    data = {"key": "value"}

    saver = JSONSaver("test.json")

    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        saver.write_to_file(data)
        assert "Произошла непредвиденная ошибка:" in fake_out.getvalue()


def test_convert_vacancy_to_dict_list_one_obj(test_vacancy1):
    saver = JSONSaver()
    assert saver.convert_vacancy_to_dict_list(test_vacancy1) == [
        {
            "name": "Python Developer",
            "vacancy_id": "123456",
            "url": "<https://hh.ru/vacancy/123456>",
            "salary": "100000-150000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        }
    ]


def test_convert_vacancy_to_dict_list_obj_list(test_vacancy1, test_vacancy2):
    vacancy = [test_vacancy1, test_vacancy2]
    saver = JSONSaver()
    assert saver.convert_vacancy_to_dict_list(vacancy) == [
        {
            "name": "Python Developer",
            "vacancy_id": "123456",
            "url": "<https://hh.ru/vacancy/123456>",
            "salary": "100000-150000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        },
        {
            "name": "Python Developer Middle",
            "vacancy_id": "123400",
            "url": "<https://hh.ru/vacancy/123400>",
            "salary": "200000 руб.",
            "requirement": "Требования: опыт работы от 3 лет...",
        },
    ]


def test_convert_vacancy_to_dict_list_not_obj():
    vacancy = "not_vacancy_object"
    saver = JSONSaver()
    assert saver.convert_vacancy_to_dict_list(vacancy) == []


def test_convert_vacancy_to_dict_list_not_obj_list():
    vacancy = ["not_vacancy_obj"]
    saver = JSONSaver()
    assert saver.convert_vacancy_to_dict_list(vacancy) == []


@patch.object(JSONSaver, "read_data_json")
@patch.object(JSONSaver, "write_to_file")
def test_add_vacancy_success(mock_write, mock_read, mock_read_dict_list, test_vacancy3, test_data_to_write):
    mock_read.return_value = mock_read_dict_list

    saver = JSONSaver("test.json")

    saver.add_vacancy(test_vacancy3)

    data_to_write = test_data_to_write
    mock_write.assert_called_once_with(data_to_write)


@patch.object(JSONSaver, "read_data_json")
@patch.object(JSONSaver, "write_to_file")
def test_add_vacancy_duplicate(mock_write, mock_read, test_data_to_write, test_vacancy3):
    mock_read.return_value = test_data_to_write

    saver = JSONSaver("test.json")

    saver.add_vacancy(test_vacancy3)

    data_to_write = test_data_to_write
    mock_write.assert_called_once_with(data_to_write)


@patch.object(JSONSaver, "read_data_json")
@patch.object(JSONSaver, "write_to_file")
def test_delete_vacancy(mock_write, mock_read, test_data_to_write, test_vacancy3, mock_read_dict_list):
    mock_read.return_value = test_data_to_write

    saver = JSONSaver("test.json")

    saver.delete_vacancy(test_vacancy3)

    data_to_write = mock_read_dict_list
    mock_write.assert_called_once_with(data_to_write)
