import re


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ("name", "vacancy_id", "url", "salary", "requirement")

    name: str
    vacancy_id: str
    url: str
    salary: str
    requirement: str

    current_vacancies = []

    def __init__(self, name=None, url=None, salary=None, requirement=None):
        """Метод инициализации экземпляра класса"""
        self.name = name
        self.url = url
        self.vacancy_id = self.get_vacancy_id()
        self.salary = self.__validate_salary(salary)
        self.requirement = requirement

    def __validate_salary(self, salary):
        """Метод валидации зарплаты"""
        pattern = r"[^0-9\-]"
        if salary is not None:
            salary = re.sub(pattern, "", salary)
            if not salary.strip():
                return "0"
            return salary
        return "0"

    def get_vacancy_id(self):
        """Метод для получения id вакансии"""
        if self.url:
            url = self.url
            url_split_str = url.split("/")[-1]
            vacancy_id = "".join(re.findall(r"\d", url_split_str))
            return str(vacancy_id)
        else:
            return None

    @classmethod
    def cast_to_object_list(cls, vacancies):
        """Класс-метод, формирующий из списка вакансий, полученных от API, список экземпляров класса"""
        cls.current_vacancies = []
        salary = None
        for vacancy in vacancies:
            if vacancy.get("salary").get("currency") == "RUR":
                salary_from_parsed = Vacancy.parse_salary(vacancy.get("salary").get("from", None))
                salary_to_parsed = Vacancy.parse_salary(vacancy.get("salary").get("to", None))

                if salary_from_parsed > 0 and salary_to_parsed == 0:
                    salary = f"{salary_from_parsed}"
                elif salary_from_parsed == 0 and salary_to_parsed > 0:
                    salary = f"{salary_to_parsed}"
                elif salary_from_parsed > 0 and salary_to_parsed > 0:
                    salary = f"{salary_from_parsed} - {salary_to_parsed}"
                else:
                    salary = "0"
                if salary != "0":
                    new_vacancy = cls(
                        name=vacancy.get("name"),
                        url=vacancy.get("alternate_url"),
                        salary=salary,
                        requirement=vacancy.get("snippet").get("requirement"),
                    )
                    cls.current_vacancies.append(new_vacancy)
        return cls.current_vacancies

    @staticmethod
    def parse_salary(salary):
        if isinstance(salary, int):
            return salary
        elif isinstance(salary, str):
            salary = salary.replace(" ", "")
            pattern = re.compile(r"\d+")
            salary_digits = re.findall(pattern, salary)
            if salary_digits:
                return int(salary_digits[0])
            else:
                return 0
        else:
            return 0

    def from_object_to_dict(self):
        """Метод для преобразования экземпляра класса в словарь"""
        vacancy_dict = {
            "name": self.name,
            "vacancy_id": self.vacancy_id,
            "url": self.url,
            "salary": f"{self.salary} руб.",
            "requirement": self.requirement,
        }
        return vacancy_dict

    def __lt__(self, other):
        """Метод сравнения вакансий по минимальной зарплате"""
        if not isinstance(other, Vacancy):
            raise TypeError(f"Нельзя сравнивать {type(other).__name__} с Vacancy")

        self_min_salary = self.get_min_salary(self.salary)
        other_min_salary = self.get_min_salary(other.salary)

        return self_min_salary < other_min_salary

    @staticmethod
    def get_min_salary(salary_str):
        """Извлекает минимальную зарплату из строки"""
        numbers = salary_str.replace(" ", "").split("-")
        if numbers:
            return int(numbers[0])

    @staticmethod
    def get_max_salary(salary_str):
        """Извлекает максимальную зарплату из строки"""
        numbers = salary_str.replace(" ", "").split("-")
        if numbers:
            return int(numbers[-1])
