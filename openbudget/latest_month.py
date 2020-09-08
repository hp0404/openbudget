import pandas as pd
from pathlib import Path


DATA = Path(__file__).resolve().parent.parent / "data" / "tables" / "2020"

di = {
    "ADMIN": str,
    "FIN_SOURCE": str,
    "INCO": str,
    "ADJUSTED": float, 
    "EXECUTED": float,
    "DATE": str
}

de = {
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

def date_slice(table):
    max_date = table["DATE"].max()
    return table.loc[table["DATE"].eq(max_date)], max_date 


if __name__ == "__main__":
    incomes = pd.read_csv(DATA / "INCOMES_2020.csv", dtype=di)
    expenses = pd.read_csv(DATA / "EXPENSES_2020.csv", dtype=de)

    latest_incomes, month = date_slice(incomes)
    latest_incomes.to_csv(DATA / f"INCOMES_{month}.csv", index=False)

    latest_expenses, month = date_slice(expenses)
    latest_expenses.to_csv(DATA / f"EXPENSES_{month}.csv", index=False)
