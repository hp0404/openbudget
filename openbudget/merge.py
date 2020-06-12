import pandas as pd
from pathlib import Path


RAW_FILES = Path(__file__).resolve().parent.parent / "data" / "tables"


def writer(files, name, item_type):
    
    if item_type == "EXPENSES":
        _dtype = {
            "ADMIN": str,
            "FIN_SOURCE": str,
            "PROG": str,
            "FUNC": str,
            "ECON": str,
            "ADJUSTED": float, 
            "EXECUTED": float,
            "EXECUTED_FIN_SOURCE_n1": float,
            "EXECUTED_FIN_SOURCE_n2": float,
            "EXECUTED_FIN_SOURCE_n6": float,
            "IS_CUMULATIVE": str,
            "DATE": str
        }
    else:
        _dtype = {
            "ADMIN": str,
            "FIN_SOURCE": str,
            "INCO": str,
            "ADJUSTED": float, 
            "EXECUTED": float,
            "DATE": str
        }
        
    for i, file in enumerate(files):
        df = pd.read_csv(file, dtype=_dtype)
        if i == 0:
            df.to_csv(RAW_FILES / name, index=False)
        else:
            df.to_csv(RAW_FILES / name, mode="a", index=False, header=False)
            
            
def concatenate(p, year, item_type):
    
    files = [p / file_name for file_name in p.glob("*.csv")]
    name = p.parent / f"{item_type}_{year}.csv"
    
    writer(files, name, item_type)
    
        
        
if __name__ == "__main__":
    
    year, item_type = "2018", "EXPENSES"
    p = RAW_FILES / year / item_type 
    concatenate(p, year, item_type)
    print(f"Done with {year + ',' + item_type}")
    
    year, item_type = "2018", "INCOMES"
    p = RAW_FILES / year / item_type 
    concatenate(p, year, item_type)
    print(f"Done with {year + ',' + item_type}")
    
    year, item_type = "2019", "EXPENSES"
    p = RAW_FILES / year / item_type 
    concatenate(p, year, item_type)
    print(f"Done with {year + ',' + item_type}")
    
    year, item_type = "2019", "INCOMES"
    p = RAW_FILES / year / item_type 
    concatenate(p, year, item_type)
    print(f"Done with {year + ',' + item_type}")
    
    year, item_type = "2020", "EXPENSES"
    p = RAW_FILES / year / item_type 
    concatenate(p, year, item_type)
    print(f"Done with {year + ',' + item_type}")
    
    year, item_type = "2020", "INCOMES"
    p = RAW_FILES / year / item_type 
    concatenate(p, year, item_type)
    print(f"Done with {year + ',' + item_type}")