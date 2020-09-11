# -*- coding: utf-8 -*-
import io
import re
import zipfile
import json

import click
import requests
import pandas as pd

from time import sleep
from itertools import product
from typing import List, Tuple

from utils import RAW_FILES, NUM_MAPPINGS


URL = "http://api.openbudget.gov.ua/api/public/getFile"


def download_data(
        api_specific_params: List[Tuple[int, int]], 
        budget_item: str = "EXPENSES", 
        year: int = 2020
    ) -> None:
    """ Завантажує та розпаковує `.zip` файли api/public/getFile.
    
    
    Parameters
    ----------
    api_specific_params : список комбінацій місяців та кодів територій
        див. https://api.openbudget.gov.ua/swagger-ui.html#/OpenBudgetPublic/getFileUsingGET
    budget_item : EXPENSES / INCOMES
    year : 2018+ 
    """
    for month, ter_id in api_specific_params:
        save_path = (RAW_FILES / str(year) / str(budget_item) / str(ter_id))
        save_path.mkdir(parents=True, exist_ok=True)

        _map = {v:k for k,v in NUM_MAPPINGS.items()}
        file_name = f"{_map.get(ter_id)}_{budget_item[:3]}_{year}_{_map.get(month)}.json"
        if (save_path / file_name).is_file():
            continue        

        params = {
            "budgetItem": budget_item, "year": year, 
            "month": month, "territoryId": ter_id
        }
        r = requests.get(URL, params, stream=True)
        if r.ok:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(save_path)
        else:
            print(f"Requests' error (status:{r.status_code}) for: {r.url}")
        sleep(0.2)
        

def main(firstmonth: int = 1, lastmonth: int = 12, year: int = 2020):
    params = [*product(range(firstmonth, lastmonth+1), range(2, 25+1))]
    for budget_item in ("EXPENSES", "INCOMES"):
        download_data(params, budget_item, year)
        

if __name__ == "__main__":
    main()