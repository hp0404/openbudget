# -*- coding: utf-8 -*-
import logging
from download import main as download_raw_data
from process import main as make_dataset
from merge import main as merge_processed_tables
from latest_month import main as save_latest_month
from tests import main as tests


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler("logger.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("Downloading raw data...")
    download_raw_data()
    logging.info("Transforming raw data into processed...")
    make_dataset()
    logging.info("Merging multiple tables into one...")
    merge_processed_tables()
    logging.info("Saving data for the last month separately...")
    save_latest_month()

    try:
        tests()
    except:
        logging.exception("TESTS FAILED.")
    
    logging.info("Done.")