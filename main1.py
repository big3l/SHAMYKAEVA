import csv


class Vacancy:
    currency_to_rub = dict(AZN=35.68, KZT=0.13, BYR=23.91, GEL=21.74, KGS=0.76, RUR=1,
                           UAH=1.64, EUR=59.90, UZS=0.0055, USD=60.66)

    def __init__(self, vacancy):
        self.name = vacancy["name"]
        self.salary_from = int(float(vacancy["salary_from"]))
        self.salary_to = int(float(vacancy["salary_to"]))
        self.salary_currency = vacancy["salary_currency"]
        self.salary_average = self.currency_to_rub[self.salary_currency] * \
                              (self.salary_from + self.salary_to) / 2
        self.area_name = vacancy["area_name"]
        self.year = int(vacancy["published_at"][:4])


class DataSet:
    def __init__(self, file_name, vacancy_name):
        self.file_name = file_name
        self.vacancy_name = vacancy_name

    def csv_reader(self):
        header = []
        salary = {}
        vacancies_number = {}
        salary_of_vacancy_names = {}
        vacancies_number_of_vacancy_names = {}
        salary_numbers = {}
        salary_cities = {}
        count_of_vacancies = 0
        with open(self.file_name, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    header = row
                    csv_header_length = len(row)
                elif '' not in row and len(row) == csv_header_length:
                    vacancy = Vacancy(dict(zip(header, row)))

                    if vacancy.year not in salary:
                        salary[vacancy.year] = [vacancy.salary_average]
                    else:
                        salary[vacancy.year].append(vacancy.salary_average)

                    if vacancy.year not in vacancies_number:
                        vacancies_number[vacancy.year] = 1
                    else:
                        vacancies_number[vacancy.year] += 1

                    if vacancy.name.find(self.vacancy_name) != -1:
                        if vacancy.year not in salary_of_vacancy_names:
                            salary_of_vacancy_names[vacancy.year] = [vacancy.salary_average]
                        else:
                            salary_of_vacancy_names[vacancy.year].append(vacancy.salary_average)

                        if vacancy.year not in vacancies_number_of_vacancy_names:
                            vacancies_number_of_vacancy_names[vacancy.year] = 1
                        else:
                            vacancies_number_of_vacancy_names[vacancy.year] += 1

                    if vacancy.area_name not in salary_cities:
                        salary_cities[vacancy.area_name] = [vacancy.salary_average]
                    else:
                        salary_cities[vacancy.area_name].append(vacancy.salary_average)

                    if vacancy.area_name not in salary_numbers:
                        salary_numbers[vacancy.area_name] = 1
                    else:
                        salary_numbers[vacancy.area_name] += 1

                    count_of_vacancies += 1

        if not salary_of_vacancy_names:
            salary_of_vacancy_names = salary.copy()
            salary_of_vacancy_names = dict([(key, []) for key, value in salary_of_vacancy_names.items()])
            vacancies_number_of_vacancy_names = vacancies_number.copy()
            vacancies_number_of_vacancy_names = dict(
                [(key, 0) for key, value in vacancies_number_of_vacancy_names.items()])

        stats, stats2, stats3, stats5 = self.stats(count_of_vacancies, salary, salary_cities, salary_numbers,
                                                   salary_of_vacancy_names)

        print('Динамика уровня зарплат по годам: ' + str(stats))
        print('Динамика количества вакансий по годам: ' + str(vacancies_number))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(stats2))
        print('Динамика количества вакансий по годам для выбранной профессии: ' +
              str(vacancies_number_of_vacancy_names))
        print('Уровень зарплат по городам (в порядке убывания): ' + str(stats3))
        print('Доля вакансий по городам (в порядке убывания): ' + str(dict(stats5[:10])))

    def stats(self, count_of_vacancies, salary, salary_cities, salary_numbers, salary_of_vacancy_names):
        stats = {}
        for year, list_of_salaries in salary.items():
            stats[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        stats2 = {}
        for year, list_of_salaries in salary_of_vacancy_names.items():
            if len(list_of_salaries) == 0:
                stats2[year] = 0
            else:
                stats2[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        stats3 = {}
        for year, list_of_salaries in salary_cities.items():
            stats3[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        stats4 = {}
        for year, list_of_salaries in salary_numbers.items():
            stats4[year] = round(list_of_salaries / count_of_vacancies, 4)
        stats4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in stats4.items()]))
        stats4.sort(key=lambda a: a[-1], reverse=True)
        stats5 = stats4.copy()
        stats4 = dict(stats4)
        stats3 = list(filter(lambda a: a[0] in list(stats4.keys()), [(key, value) for key, value in stats3.items()]))
        stats3.sort(key=lambda a: a[-1], reverse=True)
        stats3 = dict(stats3[:10])
        return stats, stats2, stats3, stats5


class InputConnect:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')

        data_set = DataSet(self.file_name, self.vacancy_name)
        data_set.csv_reader()


if __name__ == '__main__':
    InputConnect()
