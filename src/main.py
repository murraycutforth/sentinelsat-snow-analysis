from typing import List, Tuple
from dataclasses import dataclass
from math import atan2
from pathlib import Path
import logging
import queue
import concurrent.futures
import argparse

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from sentinelsat import SentinelAPI

from src.download.lta import trigger_lta
from src.download.download import download_products


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="A program to download and analyse Sentinel-2 data for snowpatch analysis")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-D", action="store_true", help="DOWNLOAD mode- run this to cache data")
    group.add_argument("-A", action="store_true", help="ANALYSIS mode- run this to analyse data after downloading")

    dgroup = parser.add_argument_group(title="Args for data download")
    dgroup.add_argument("--data_dir", type=str, help="Path to dir where data should be cached", default=".")
    dgroup.add_argument("--geojson_path", type=str, help="Path to geojson file containing polygons covering all areas which data should be downloaded for")
    dgroup.add_argument("--download_full", action="store_true", help="Store the full tile, rather than cropping to ROI around polygon")

    agroup = parser.add_argument_group(title="Args for data analysis")

    args = parser.parse_args()
    return args


def load_product_list():
    # TODO: temp
    return pd.read_csv("s2_T30VVJ_MSI2A_under50cloud.csv", header=0, index_col=0).index


def main():
    args = parse_args()

    if args.D:
        logger.info("DOWNLOADING DATA")

        # TODO: feed in API key through args, rather than here
        user = "murraycutforth"
        password = "6j6xRHZzAu8X"
        api = SentinelAPI(user, password)

        # TODO
        # Either read in csv list of products to download
        # Or read a geojson file, and run a query based on that footprint, to get the list of product ids
        prod_ids = load_product_list()

        # TODO
        # Make these go in parallel, so data is downloaded as it becomes available
        trigger_lta(prod_ids, api)
        download_products(api, prod_ids, args)
        


        assert 0

    else:
        assert args.A
        logger.info("ANALYSING DATA")

        assert 0





        #title = product_info["title"]

        #logger.info(f"{title}. Online = {online}")

        #if online:
        #    api.download(prod_id)

        #else:
        #    lta = api.trigger_offline_retrieval(prod_id)
        #    logger.info(f"Triggered offline retrieval with return: {lta}")


        #break



if __name__ == "__main__":
    main()
