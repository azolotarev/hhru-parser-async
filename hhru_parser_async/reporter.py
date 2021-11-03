import json
import os
import re
from collections import defaultdict

from hhru_parser_async.api_calls import CACHE_DIR

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html: str) -> str:
    """
    Removes html tags from string

    Args:
        raw_html (str): string with those pesky tags

    Returns:
        str: cleaned string
    """
    return re.sub(CLEANR, '', raw_html)


def vacancy_to_str(vacancy: dict) -> str:
    """
    Formats vacancy json to string for later use

    Args:
        vacancy (dict): json with vacancy info

    Returns:
        str: formatted string
    """
    # add vacancy info
    result = vacancy['name'] + ' ' + vacancy['alternate_url']
    # split by new_lines
    s = vacancy['description'].split('<p>')

    # clean lines
    s = [cleanhtml(item.replace('</p>', '')) for item in s]
    x = []
    for item in list(s):
        x += [i.strip() for i in item.split('  ')]
    s = list(filter(bool, x))

    # add salary
    if vacancy['salary']:
        result += f"\nЗарплата: {vacancy['salary']['from']} - {vacancy['salary']['to']}"

    # format
    pars = defaultdict(lambda: [])
    keyword = ''
    for line in s:
        if line[-1] == ':':
            keyword = line
        elif keyword != '':
            pars[keyword].append(line.replace('&quot;', ''))
    # results
    for key, value in pars.items():
        result += '\n\n' + key
        result += ''.join(['\n* ' + v for v in value])

    return result


def read_cache(cache_dir: str = CACHE_DIR) -> str:
    all_vacancies = ''
    for file in os.listdir(cache_dir):
        with open(os.path.join(cache_dir, file), 'r') as f:
            vacancy = json.loads(f.read())
        all_vacancies += vacancy_to_str(vacancy)
        all_vacancies += '\n\n\n'
    return all_vacancies
