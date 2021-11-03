import asyncio

from hhru_parser_async import api_calls

if __name__ == '__main__':
    query = input('Please enter your query:\n>> ')
    total_vacancies = api_calls.get_total_vacancies(query)
    proceed = input(f'Found {total_vacancies} vacancies. Proceed? y/n\n>> ')
    if proceed.lower() != 'y':
        exit()
    vacancies_ids = asyncio.run(
        api_calls.get_vacancy_ids(query, total_vacancies))
    # TODO: clear cache
    asyncio.run(api_calls.get_all_vacancies(vacancies_ids))
    print('Done.')
    # TODO: form report
