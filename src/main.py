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

from src.download.download import download_products


logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="A program to download and analyse Sentinel-2 data for snowpatch analysis")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-D", action="store_true", help="DOWNLOAD mode- run this to cache data")
    group.add_argument("-A", action="store_true", help="ANALYSIS mode- run this to analyse data after downloading")

    dgroup = parser.add_argument_group(title="Args for data download")
    dgroup.add_argument("--data_dir", type=str, help="Path to dir where data should be cached", default=".")
    dgroup.add_argument("--geojson_path", type=str, help="Path to geojson file containing polygons covering all areas which data should be downloaded for")
    dgroup.add_argument("--download_full", action="store_true", help="Store the full data product, rather than just the 20m SCL band. Uses WAY more disk space.")
    dgroup.add_argument("--api_user", type=str, default="murraycutforth", help="Username for Copernicus Sentinel API")
    dgroup.add_argument("--api_password", type=str, default="6j6xRHZzAu8X", help="Password for Copernicus Sentinel API")

    agroup = parser.add_argument_group(title="Args for data analysis")

    args = parser.parse_args()
    return args


def load_product_list():
    # TODO: temp
    return pd.read_csv("s2_T30VVJ_MSI2A_under50cloud.csv", header=0, index_col=0).index


def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s")
    args = parse_args()

    if args.D:
        logger.info("DOWNLOADING DATA")

        api = SentinelAPI(args.api_user, args.api_password)

        # TODO
        # Either read in csv list of products to download
        # Or read a geojson file, and run a query based on that footprint, to get the list of product ids
        prod_ids = load_product_list()

        download_products(api, prod_ids, args)

        logger.info("All products downloaded")
        logger.info("Code completed normally")
        return

    else:
        assert args.A
        logger.info("ANALYSING DATA")

        assert 0


if __name__ == "__main__":
    main()
