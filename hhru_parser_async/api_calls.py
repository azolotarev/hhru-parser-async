import asyncio
import json
from json.decoder import JSONDecodeError
from typing import List

import requests
import tqdm.asyncio
from aiohttp import ClientSession

BASE_URL = "https://api.hh.ru"
CACHE_FOLDER = "cache"


def get_total_vacancies(query: str, area: int = 1) -> int:
    """
    Get number of vacancies found

    Args:
        query (str): user search query, e.g. "python", "java", "js middle", etc.
        area (int, optional): ID of area from https://api.hh.ru/areas/. Defaults to 1 - Moscow

    Returns:
        int: number of vacancies
    """
    url = f"{BASE_URL}/vacancies?text={query}&area={area}"
    result = requests.get(url)
    if result.status_code == 200:
        return int(result.json()['found'])
    else:
        raise RuntimeError(
            f'Could not resolve requested URL (Status {result.status_code}):\n{url}')


async def get_vacancy_ids(query: str, total_vacancies: int, area: int = 1) -> List[int]:
    """
    Get list of ids of all vacancies that match the query

    Args:
        query (str): user search query, e.g. "python", "java", "js middle", etc.
        total_vacancies (int): number, output of get_total_vacancies
        area (int, optional): ID of area from https://api.hh.ru/areas/. Defaults to 1 - Moscow

    Returns:
        List[int]: list with vacancy ids
    """
    ids = List[int]
    per_page = 100
    pages = -(total_vacancies // -per_page)
    url = f"{BASE_URL}/vacancies?text={query}&area={area}&per_page={per_page}"
    arrays = await asyncio.gather(*[get_ids(url+f"&page={page}") for page in range(pages)])
    return [item for sublist in arrays for item in sublist]


async def get_ids(url: str) -> List[int]:
    """
    Load all vacancy ids from a search page

    Args:
        url (str): search url with page selected

    Returns:
        List[int]: vacancy ids for that page
    """
    async with ClientSession() as session:
        async with session.get(url) as response:
            result = await response.read()
            vacancies = json.loads(result.decode('utf-8'))['items']
            return [int(item['id']) for item in vacancies]


async def get_all_vacancies(vacancies_ids: List[int]) -> None:
    """
    Loads all vacancy jsons to cache

    Args:
        vacancies_ids (List[int]): list of vacancy ids from get_vacancy_ids
    """
    print('Loading vacancies...')
    for f in tqdm.asyncio.tqdm.as_completed([get_vacancy_info(id_) for id_ in vacancies_ids]):
        await f


async def get_vacancy_info(id_: int) -> None:
    """
    Loads vacancy json and saves it to cache

    Args:
        id_ (int): vacancy id
    """
    url = f"{BASE_URL}/vacancies/{id_}"
    async with ClientSession() as session:
        async with session.get(url) as response:
            result = await response.read()
            info = json.loads(result.decode('utf-8'))
            with open(f'{CACHE_FOLDER}/{id_}.json', 'w') as f:
                json.dump(info, f)
