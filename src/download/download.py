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
from sentinelsat import SentinelAPI, make_path_filter


logger = logging.getLogger(__name__)


def download_products(api: SentinelAPI, prod_ids: List, args: argparse.Namespace):
    """Download all products
    """
    cdir = args.data_dir

    if args.download_full:
        for pid in prod_ids:
            api.download(pid, cdir)
    else:
        path_filter = make_path_filter("*SCL_20m.jp2")
        directory_path = args.data_dir

        for pid in prod_ids:
            api.download(pid, cdir, nodefilter=path_filter)

