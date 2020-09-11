# -*- coding: utf-8 -*-
import click
import logging
from download import main as download_raw_data
from process import main as make_dataset
from merge import main as merge_processed_tables
from latest_month import main as save_latest_month
from tests import main as tests


@click.command()
@click.option("--firstmonth", prompt="First month:", default=1)
@click.option("--lastmonth", prompt="Last month:", default=12)
@click.option("--year", prompt="Year:", default=2020)
def cli(firstmonth, lastmonth, year):

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler("logger.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("Downloading raw data...")
    download_raw_data(firstmonth, lastmonth, year)
    logging.info("Transforming raw data into processed...")
    make_dataset(year)
    logging.info("Merging multiple tables into one...")
    merge_processed_tables(year)
    logging.info("Saving data for the last month separately...")
    save_latest_month(year)
    try:
        tests(year)
        logging.info("Passed tests.")
    except:
        logging.exception("TESTS FAILED.")
    
    logging.info("Done.")


if __name__ == "__main__":
    cli()