import json
import pandas as pd
from pathlib import Path

from transform import get_cumulative, transform


RAW_FILES = Path(__file__).resolve().parent.parent / "data" / "api_response"
PROCESSED = Path(__file__).resolve().parent.parent / "data" / "tables"


def pathlib_walk(p, outputs):
    
    for directory in p.iterdir():
        
        files = [directory / file_name for file_name in directory.glob("*.json")]
        
        param_type, save_name = directory.parts[-2:]
        
        cumulative_dict = get_cumulative(files, item_type=param_type)
        noncumulative = transform(cumulative_dict, item_type=param_type)
        
        noncumulative.to_csv(outputs / f"{save_name}.csv", index=False)
        
        


if __name__ == "__main__":
    
    inputs  = RAW_FILES / "2018" / "INCOMES"
    outputs = PROCESSED / "2018" / "INCOMES"
    outputs.mkdir(parents=True, exist_ok=True)
    pathlib_walk(inputs, outputs)