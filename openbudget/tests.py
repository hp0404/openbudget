import pandas as pd
from utils import get_cumulative, RAW_FILES, PROCESSED
from latest_month import slice_maxdate


DTYPES = {"ADMIN": str, "INCO": str, "ECON": str}


def main(year: str = "2020"):

    TRANSFORMED = PROCESSED / str(year)
    RAW_INC_FILES = RAW_FILES / str(year) / "INCOMES" / "10"
    RAW_EXP_FILES = RAW_FILES / str(year) / "EXPENSES" / "10"

    def incomes(year: str = "2020"):
        transformed = pd.read_csv(TRANSFORMED / f"INCOMES_{year}.csv", dtype=DTYPES)
        test1 = transformed.loc[
            transformed["ADMIN"].eq("10518000000") & transformed["INCO"].eq("10000000")
        ]

        validation = pd.read_csv(TRANSFORMED / "INCOMES" / "10.csv", dtype=DTYPES)
        test2 = validation.loc[
            validation["ADMIN"].eq("10518000000") & validation["INCO"].eq("10000000")
        ]
        # merged correctly
        assert test2["EXECUTED"].sum().round(2) == test1["EXECUTED"].sum().round(2)

        cumulative_dict = get_cumulative(
            RAW_INC_FILES.rglob("*.json"), item_type="INCOMES"
        )
        last_month = [*cumulative_dict.keys()][-1]
        cumulative_df = cumulative_dict[last_month]
        test3 = cumulative_df.loc[
            cumulative_df["ADMIN"].eq("10518000000")
            & cumulative_df["INCO"].eq("10000000")
        ]

        # transformed correctly
        # EXECUTED
        assert test3["EXECUTED"].sum().round(2) == test1["EXECUTED"].sum().round(2)

        # ADJUSTED
        test1_latest_month, _ = slice_maxdate(test1)
        assert test3["ADJUSTED"].sum().round(2) == test1_latest_month[
            "ADJUSTED"
        ].sum().round(2)

    def expenses(year: str = "2020"):
        transformed = pd.read_csv(TRANSFORMED / f"EXPENSES_{year}.csv", dtype=DTYPES)
        test1 = transformed.loc[
            transformed["ADMIN"].eq("10518000000") & transformed["ECON"].ne("0000")
        ]

        validation = pd.read_csv(TRANSFORMED / "EXPENSES" / "10.csv", dtype=DTYPES)
        test2 = validation.loc[
            validation["ADMIN"].eq("10518000000") & validation["ECON"].ne("0000")
        ]
        assert test2["EXECUTED"].sum().round(2) == test1["EXECUTED"].sum().round(2)

        cumulative_dict = get_cumulative(
            RAW_EXP_FILES.rglob("*.json"), item_type="EXPENSES"
        )
        last_month = [*cumulative_dict.keys()][-1]
        cumulative_df = cumulative_dict[last_month]
        test3 = cumulative_df.loc[
            cumulative_df["ADMIN"].eq("10518000000") & cumulative_df["ECON"].ne("0000")
        ]

        # transformed correctly
        # EXECUTED
        assert test3["EXECUTED"].sum().round(2) == test1["EXECUTED"].sum().round(2)

        # ADJUSTED
        test1_latest_month, _ = slice_maxdate(test1)
        assert test3["ADJUSTED"].sum().round(2) == test1_latest_month[
            "ADJUSTED"
        ].sum().round(2)

    incomes(year)
    expenses(year)


if __name__ == "__main__":
    main()
