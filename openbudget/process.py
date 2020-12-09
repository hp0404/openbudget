# -*- coding: utf-8 -*-
import pathlib
from utils import RAW_FILES, PROCESSED, get_cumulative, transform


def pathlib_walk(
    p: pathlib.WindowsPath, outputs: pathlib.WindowsPath, year: int
) -> None:
    """ Проходить по папках з .json та перетворює їх на таблиці. """
    for directory in p.iterdir():
        files = [directory / file_name for file_name in directory.glob("*.json")]
        param_type, save_name = directory.parts[-2:]
        cumulative_dict = get_cumulative(files, item_type=param_type)
        noncumulative = transform(cumulative_dict, item_type=param_type, year=year)
        noncumulative.to_csv(outputs / f"{save_name}.csv", index=False)


def process_raw_data(year: str, item: str) -> None:
    """ Обгортка для pathlib_walk, яка визначає потрібний шлях"""
    inputs = RAW_FILES / year / item
    outputs = PROCESSED / year / item
    outputs.mkdir(parents=True, exist_ok=True)
    pathlib_walk(inputs, outputs, year)


def main(year):
    for pairs in [(str(year), "EXPENSES"), (str(year), "INCOMES")]:
        process_raw_data(*pairs)


if __name__ == "__main__":
    main()
