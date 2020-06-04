import json
import pandas as pd
from typing import Any, Dict


def get_cumulative(
    files: Dict[str, Any], 
    item_type: str ="EXPENSES"
) -> Dict[int, pd.DataFrame]:
    """ Перетворює щомісячні json на словник датафреймів. 
    Значення залишаються кумулятивними.
    
    
    Parameters
    ----------
        files : JSON
            Відповідь АРІ openbudget.
        item_type : str
            Маркер типу файлу (видатки / доходи)
    """
    
    _mappings = {
        "01": 1,
        "02": 2,
        "03": 3,
        "04": 4,
        "05": 5,
        "06": 6,
        "07": 7,
        "08": 8,
        "09": 9,
        "10": 10,
        "11": 11,
        "12": 12
    }
    
    d = dict()
    for file in files:        
        with open(file, "r") as f:
            data = json.load(f)
        
        month_string = str(file).split("/")[-1].split("_")[-1].split(".")[0]
        month = _mappings.get(month_string)
        
        df = pd.json_normalize(data)
        df["MONTH"] = month
        
        if item_type == "EXPENSES":
            df["IS_CUMULATIVE"] = df["ECON"].eq("0000").astype(int)
        
        d[month] = df
    
    return d


def transform(
    d: Dict[int, pd.DataFrame], 
    item_type: bool = "EXPENSES"
) -> pd.DataFrame:
    """Перетворює словник датафреймів на єдину таблицю та 
    перетворює кумулятивні значення на некумулятивні щомісячні
    
    
    Parameters
    ----------
        d : Dict[int, pd.DataFrame]
            Словник датафреймів з кумулятивними значеннями
        item_type : str
            Маркер типу файлу (видатки / доходи)
    """
    
    current_range = list(d.keys())[::-1]
    previous_range = [m-1 for m in current_range]
    
    if item_type == "EXPENSES":
        idxs = ["ADMIN", "FIN_SOURCE", "PROG", "FUNC", "ECON"]
    else:
        idxs = ["ADMIN", "FIN_SOURCE", "INCO"]
    
    data = dict()
    for current, previous in zip(current_range, previous_range):
        if previous != 0:
            tmp = (
                d[current].set_index(idxs).subtract(d[previous].set_index(idxs), fill_value=0)
            ).reset_index()
            
            tmp["MONTH"] = current
            if item_type == "EXPENSES":
                tmp["IS_CUMULATIVE"] = tmp["ECON"].eq("0000").astype(int)
            
            data[current] = tmp
        else:
            data[current] = d[1]
    
    return pd.concat([*data.values()], ignore_index=False)[::-1]