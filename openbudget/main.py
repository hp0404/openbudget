# -*- coding: utf-8 -*-
import json
import pandas as pd
from pathlib import Path

from transform import get_cumulative, transform


RAW_FILES = Path(__file__).resolve().parent.parent / "data" / "api_response"
PROCESSED = Path(__file__).resolve().parent.parent / "data" / "tables"


def pathlib_walk(p, outputs, year):
    
    for directory in p.iterdir():
        
        files = [directory / file_name for file_name in directory.glob("*.json")]
        
        param_type, save_name = directory.parts[-2:]
        
        cumulative_dict = get_cumulative(files, item_type=param_type)
        noncumulative = transform(cumulative_dict, item_type=param_type, year=year)
        noncumulative.to_csv(outputs / f"{save_name}.csv", index=False)
        
        
def main():
    
    inputs  = RAW_FILES / YEAR / ITEM 
    outputs = PROCESSED / YEAR / ITEM
    outputs.mkdir(parents=True, exist_ok=True)
    pathlib_walk(inputs, outputs, YEAR)
    print(f"Done with {YEAR + ',' + ITEM}")


if __name__ == "__main__":
    
    YEAR = "2020"
    ITEM = "EXPENSES"
    main()
   
    YEAR = "2020"
    ITEM = "INCOMES"
    main()