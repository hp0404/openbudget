# -*- coding: utf-8 -*-
import io
import re
import zipfile
import json

import requests
import pandas as pd

from time import sleep
from itertools import product
from typing import List, Tuple

from utils import RAW_FILES


URL = "http://api.openbudget.gov.ua/api/public/getFile"


def download_data(
        api_specific_params: List[Tuple[int, int]], 
        budget_item: str = "EXPENSES", 
        year: int = 2019
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
        

def main():
    params = [*product(range(1,7+1), range(2, 25+1))]
    for budget_item in ("EXPENSES", "INCOMES"):
        download_data(params, budget_item, 2020)
        

if __name__ == "__main__":
    main()