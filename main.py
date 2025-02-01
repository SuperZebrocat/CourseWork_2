from src.utils import (
    get_vacancies_from_api,
    filter_vacancies,
    filter_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)

from src.json_saver import JSONSaver


# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()


def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите ключевое слово для поиска вакансий: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: \n")  # Пример: 100000 - 150000

    vacancies_list = get_vacancies_from_api(search_query)

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = filter_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)

    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
