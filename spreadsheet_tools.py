import openpyxl


def create_spreadsheet(data: list[dict[str, str]], filepath: str = 'data.xlsx') -> None:
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = 'Вакансии'

    ws.append(['Вакансия', 'Ссылка', 'Работодатель', 'Рейтинг работодателя', 'Зарплата', 'Метаданные', 'Навыки', 'Дата'])

    for row in data:
        ws.append(list(row.values()))

    wb.save(filepath)
    wb.close()
