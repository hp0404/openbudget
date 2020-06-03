import os, json
import pandas as pd


PATH = "./../data/api_response/"
DIR = os.listdir(PATH)
ZVEDENYI = (
    "02000000000", "03000000000", "04000000000", "05000000000", "06000000000",
    "07000000000", "08000000000", "09000000000", "10000000000", "11000000000",
    "12000000000", "13000000000", "14000000000", "15000000000", "16000000000",
    "17000000000", "18000000000", "19000000000", "20000000000", "21000000000",
    "22000000000", "23000000000", "24000000000", "25000000000", "26000000000"
)



def get_cumulative(files):
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
        
        month_string = file.split("/")[-1].split("_")[-1].split(".")[0]
        month = _mappings.get(month_string)
        
        df = pd.json_normalize(data)
        df["MONTH"] = month
        d[month] = df.loc[df["ADMIN"].isin(ZVEDENYI) & df["ECON"].ne("0000")]
    
    return d


def transform(d):
    
    current_range = list(d.keys())[::-1]
    previous_range = [m-1 for m in current_range]
    
    idxs = ["ADMIN", "FIN_SOURCE", "PROG", "FUNC", "ECON"]
    
    data = dict()
    for current, previous in zip(current_range, previous_range):
        if previous != 0:
            tmp = (
                d[current].set_index(idxs).subtract(
                    d[previous].set_index(idxs), fill_value=0)
            ).reset_index()
            tmp["MONTH"] = current
            data[current] = tmp
        else:
            data[current] = d[1]
    
    return data

        
def main():
    
    files = [os.path.join(PATH, f) for f in DIR]
    cumulative_dict = get_cumulative(files)
    noncumulative = transform(cumulative_dict)
    
    result = pd.concat([*noncumulative.values()], ignore_index=False)
    
    result.to_excel("Вінницька_некумулятивно.xlsx", index=False)
    

if __name__ == "__main__":
    main()