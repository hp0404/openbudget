import io
import re
import zipfile
import json

import requests
import pandas as pd

from time import sleep
from pathlib import Path
from itertools import product, chain


PATH = Path(__file__).resolve().parent.parent / "data" 

# паттерни для ідентифікації завантажених файлів
TER_ID_PATTERN = re.compile(r"(\d{2})_(EXP|INC)")
MONTH_ID_PATTERN = re.compile(r"(\d{1,2}).json")

LAND = ( # коди, що пов'язані з землею
    "18010500",
    "18010600",
    "18010700",
    "18010800",
    "18010900"
)

ZVEDENYI = (
    "02000000000",
    "03000000000",
    "04000000000",
    "05000000000",
    "06000000000",
    "07000000000",
    "08000000000",
    "09000000000",
    "10000000000",
    "11000000000",
    "12000000000",
    "13000000000",
    "14000000000",
    "15000000000",
    "16000000000",
    "17000000000",
    "18000000000",
    "19000000000",
    "20000000000",
    "21000000000",
    "22000000000",
    "23000000000",
    "24000000000",
    "25000000000",
    "26000000000"
)

REGIONS = {
    "02000000000" : "Вінницька",
    "03000000000" : "Волинська",
    "04000000000" : "Дніпропетровська",
    "05000000000" : "Донецька",
    "06000000000" : "Житомирська",
    "07000000000" : "Закарпатська",
    "08000000000" : "Запорізька",
    "09000000000" : "Івано-Франківська",
    "10000000000" : "Київська",
    "11000000000" : "Кіровоградська",
    "12000000000" : "Луганська",
    "13000000000" : "Львівська",
    "14000000000" : "Миколаївська", 
    "15000000000" : "Одеська",
    "16000000000" : "Полтавська",
    "17000000000" : "Рівненська",
    "18000000000" : "Сумська",
    "19000000000" : "Тернопільська",
    "20000000000" : "Харківська",
    "21000000000" : "Херсонська",
    "22000000000" : "Хмельницька",
    "23000000000" : "Черкаська",
    "24000000000" : "Чернівецька",
    "25000000000" : "Чернігівська",
}


def download_data(api_specific_params, budget_item="EXPENSES", year=2019):
    """ Завантажує та розпаковує `.zip` файли, отримані з api/public/getFile.
    
    
    Parameters
    ----------
    api_specific_params : список комбінацій місяців та кодів територій
        див. https://api.openbudget.gov.ua/swagger-ui.html#/OpenBudgetPublic/getFileUsingGET
        
    >>> months = list(range(1,12+1)) # увесь рік
    >>> ids = [16] # Наприклад, тільки полтавська область 
    >>> params = list(product(months, ids))
    >>> download_data(api_specific_params=params, budget_item="EXPENSES", year=2019)
    """
    
    url = "http://api.openbudget.gov.ua/api/public/getFile"
    for month, ter_id in api_specific_params:
        params = {
            "budgetItem": budget_item, "year": year, 
            "month": month, "territoryId": ter_id
        }
        r = requests.get(url, params, stream=True)
        if r.ok:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(PATH / "api_response")
        else:
            print(f"Помилка, url: {r.url}")
        sleep(1)
            

def _dataframe_generator(params):    
    """ Генерує pd.DataFrame з .json файлу
    * додає колонки місяця та області
    * відфільтровує лише обласні бюджети
    
    Використовую всередині функції `extract_data`
    
    
    Parameters
    ----------
    params : шлях до файлу, код території, місяць
        ці параметри визначаються у функції `extract_data`
    """
    
    for fpath, territory_id, month_id in params:
        with open(fpath, "r") as f:
            data = json.load(f)
            
        df = pd.json_normalize(data)
        df["MONTH_CUMMULATIVE"] = month_id
        df["TERRITORY_ID"] = territory_id
        
        # Повертаю області та зведені
        df = df.loc[df["ADMIN"].isin(ZVEDENYI)]
        
        yield df
        

def extract_data(word="EXP", month="01", year="2019"):
    """ Створення остаточної таблиці
    

    Parameters
    ----------
    word : слово, за яким визначається тип файлу:
        EXP - expenses, видатки
        INC - incomes, доходи    
    """
    files_path = [PATH / f for f in PATH.rglob("*.json") if f"{word}_{year}_{month}" in f]
    
    ter_id, month_id = [], []
    for f in files_path:
        ter_id.append(TER_ID_PATTERN.search(f).group(1))
        month_id.append(MONTH_ID_PATTERN.search(f).group(1))
    
    params = list(zip(files_path, ter_id, month_id))
    return pd.concat(_dataframe_generator(params), ignore_index=True)


def download_files():
        
    #params = [(3, region) for region in range(2, 25+1)]
    params = [(12, region) for region in range(2, 25+1)]
    download_data(params, budget_item="INCOMES", year=2018)
    download_data(params, budget_item="INCOMES", year=2019)
    download_data(params, budget_item="INCOMES", year=2020)
    download_data(params, budget_item="EXPENSES", year=2018)
    download_data(params, budget_item="EXPENSES", year=2019)
    download_data(params, budget_item="EXPENSES", year=2020)
    
    
def single_case():
    
    params = [(month, 2) for month in range(1, 12+1)]
    download_data(params, budget_item="EXPENSES", year=2018)
    


if __name__ == "__main__":
    single_case()