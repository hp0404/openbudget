import json
import pandas as pd
from pathlib import Path


PATH = Path(__file__).resolve().parent.parent / "data"


def get_cumulative(files, item_type="EXPENSES"):
    """
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
        
        file_as_str = str(file)
        month_string = file_as_str.split("/")[-1].split("_")[-1].split(".")[0]
        month = _mappings.get(month_string)
        
        df = pd.json_normalize(data)
        df["MONTH"] = month
        
        # if expenses
        if item_type == "EXPENSES":
            df["IS_CUMULATIVE"] = (df["ECON"].eq("0000")).astype(int)
        
        d[month] = df
    
    return d


def subtraction(d):
    
    current_range = list(d.keys())[::-1]
    previous_range = [m-1 for m in current_range]
    
    for current, previous in zip(current_range, previous_range):
        
        current_month = d[current].set_index(idxs)
        previous_month = d[previous].set_index(idxs)
        
        if previous != 0:
            tmp = (
                current_month.subtract(previous_month, fill_value=0)
                .reset_index()
            )
            tmp["MONTH"] = current
            data[current] = tmp
        else:
            data[current] = d[1]


def transform(d, item_type="EXPENSES"):
    """
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
            data[current] = tmp
        else:
            data[current] = d[1]
    
    return pd.concat([*data.values()], ignore_index=False)[::-1]


def main():
    pass


if __name__ == "__main__":
    main()