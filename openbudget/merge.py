# -*- coding: utf-8 -*-
import pathlib
import pandas as pd
from typing import List
from utils import PROCESSED, DTYPE_EXP, DTYPE_INC


def writer(
        files: List[pathlib.WindowsPath], 
        name: str, 
        item_type: str
    ) -> None:
    """ Зводить усі файли в один по частинах """
    _dtype = DTYPE_EXP if item_type == "EXPENSES" else DTYPE_INC        
    for idx, f in enumerate(files):
        df = pd.read_csv(f, dtype=_dtype)
        if idx == 0:
            df.to_csv(PROCESSED / name, index=False)
        else:
            df.to_csv(PROCESSED / name, mode="a", index=False, header=False)
            
            
def merge(p: pathlib.WindowsPath, year: str, item_type: str):
    """ Обгортка для writer, котра визнає шлях"""
    files = [p / file_name for file_name in p.glob("*.csv")]
    name = p.parent / f"{item_type}_{year}.csv"
    writer(files, name, item_type)
    
        
def main():
    for pairs in [("2020", "EXPENSES"), ("2020", "INCOMES")]:
        year, item_type = pairs
        path = PROCESSED / year / item_type
        merge(path, year, item_type)


if __name__ == "__main__":
    main()