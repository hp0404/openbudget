import pandas as pd
from utils import PROCESSED, DTYPE_INC, DTYPE_EXP


PATH = PROCESSED / "2020"


def slice_maxdate(table: pd.DataFrame) -> pd.DataFrame:
    max_date = table["DATE"].max()
    return table.loc[table["DATE"].eq(max_date)], max_date 


def main() -> None:
    """ Відфільтровує та зберігає окремо дані за останній місяць. """
    incomes = pd.read_csv(PATH / "INCOMES_2020.csv", dtype=DTYPE_INC)
    expenses = pd.read_csv(PATH / "EXPENSES_2020.csv", dtype=DTYPE_EXP)

    latest_incomes, month = slice_maxdate(incomes)
    latest_incomes.to_csv(PATH / f"INCOMES_{month}.csv", index=False)

    latest_expenses, month = slice_maxdate(expenses)
    latest_expenses.to_csv(PATH / f"EXPENSES_{month}.csv", index=False)


if __name__ == "__main__":
    main()