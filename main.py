import parser
import spreadsheet_tools

if __name__ == '__main__':
    vacancies: list[dict[str, str]] = parser.parse('Python')
    spreadsheet_tools.create_spreadsheet(vacancies)
