from typing import List, Tuple
from dataclasses import dataclass
from math import atan2
from pathlib import Path
import logging
import queue
import concurrent.futures
import argparse
import time

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from sentinelsat import SentinelAPI, make_path_filter


logger = logging.getLogger(__name__)


def _download_prod_inner(prod_id, cdir, api, download_full, retry_delay=1800):
    logger.info(f"Attempting download of {prod_id}")

    while True:
        try:
            if download_full:
                api.download(prod_id, cdir)
            else:
                path_filter = make_path_filter("*SCL_20m.jp2")
                api.download(prod_id, cdir, nodefilter=path_filter)
            break
        except Exception as e:
            logger.error(f"Download failed with {e}. Retrying in 30mins.")
            time.sleep(retry_delay)


def download_products(api: SentinelAPI, prod_ids: List, args: argparse.Namespace):
    """Download all products
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for pid in prod_ids:
            executor.submit(_download_prod_inner, pid, args.data_dir, api, args.download_full)

    logger.info("All products downloaded")

