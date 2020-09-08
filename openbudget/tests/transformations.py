import pandas as pd 
from pathlib import Path


PATH = Path(__file__).resolve().parent.parent.parent / "data" / "tables" / "2020"
DTYPES = {"ADMIN": str, "INCO":str, "ECON":str}


def incomes():
    transformed = pd.read_csv(PATH / "INCOMES_2020.csv", dtype=DTYPES)
    test1 = transformed.loc[
        transformed["ADMIN"].eq("10518000000") & 
        transformed["INCO"].eq("10000000")
    ]

    validation = pd.read_csv(PATH / "INCOMES" / "10.csv", dtype=DTYPES)
    test2 = validation.loc[
        validation["ADMIN"].eq("10518000000") & 
        validation["INCO"].eq("10000000")
    ]

    assert test2["EXECUTED"].sum().round(2) == test1["EXECUTED"].sum().round(2)


def expenses():
    transformed = pd.read_csv(PATH / "EXPENSES_2020.csv", dtype=DTYPES)
    test1 = transformed.loc[
        transformed["ADMIN"].eq("10518000000") & 
        transformed["ECON"].ne("0000")
    ]

    validation = pd.read_csv(PATH / "EXPENSES" / "10.csv", dtype=DTYPES)
    test2 = validation.loc[
        validation["ADMIN"].eq("10518000000") & 
        validation["ECON"].ne("0000")
    ]
    assert test2["EXECUTED"].sum().round(2) == test1["EXECUTED"].sum().round(2)


if __name__ == "__main__":
    incomes()
    expenses()
