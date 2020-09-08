# -*- coding: utf-8 -*-
import io
import re
import zipfile
import json

import requests
import pandas as pd

from time import sleep
from pathlib import Path
from itertools import product


PATH = Path(__file__).resolve().parent.parent / "data" 


def download_data(api_specific_params, budget_item="EXPENSES", year=2019):
    """ Завантажує та розпаковує `.zip` файли, отримані з api/public/getFile.
    
    
    Parameters
    ----------
    api_specific_params : список комбінацій місяців та кодів територій
        див. https://api.openbudget.gov.ua/swagger-ui.html#/OpenBudgetPublic/getFileUsingGET
    """
    
    url = "http://api.openbudget.gov.ua/api/public/getFile"
    for month, ter_id in api_specific_params:
        
        save_path = (PATH / "api_response" / str(year) / str(budget_item) / str(ter_id))
        save_path.mkdir(parents=True, exist_ok=True)
        
        params = {
            "budgetItem": budget_item, "year": year, 
            "month": month, "territoryId": ter_id
        }
        r = requests.get(url, params, stream=True)
        if r.ok:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(save_path)
        else:
            print(f"Requests' error (status:{r.status}) for: {r.url}")
        sleep(0.5)
        

if __name__ == "__main__":
    params = product(range(1,7+1), range(2, 25+1))
    download_data(params, "INCOMES", 2020)
