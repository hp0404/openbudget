import pandas as pd
from pathlib import Path


RAW_FILES = Path(__file__).resolve().parent.parent / "data" / "tables"


def writer(files, name):
    for i, file in enumerate(files):
        df = pd.read_csv(file)
        if i == 0:
            df.to_csv(RAW_FILES / name, index=False)
        else:
            df.to_csv(RAW_FILES / name, mode="a", index=False, header=False)
            
            
def concatenate(p, year, item_type):
    
    files = [p / file_name for file_name in p.glob("*.csv")]
    name = p.parent / f"{item_type}_{year}.csv"
    
    writer(files, name)
    
        
        
if __name__ == "__main__":
    
    year, item_type = "2020", "INCOMES"
    p = RAW_FILES / year / item_type 
    
    concatenate(p, year, item_type)