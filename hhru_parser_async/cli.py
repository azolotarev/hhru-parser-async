import asyncio

from hhru_parser_async import api_calls

while True:
    query = input('Please enter your query:\n>> ')
    total_vacancies = api_calls.get_total_vacancies(query)
    proceed = input(f'Found {total_vacancies} vacancies. Proceed? Y/N\n>> ')
    if proceed.upper() != 'Y':
        continue
    vacancies_ids = asyncio.run(
        api_calls.get_vacancy_ids(query, total_vacancies))
    # get full vacancy info
    asyncio.run(api_calls.get_all_vacancies(vacancies_ids))
    print('Done.')
    exit()
