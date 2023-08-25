from typing import List, Tuple
from pathlib import Path
import logging
import concurrent.futures
import argparse

import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)


def _trigger_lta_inner(prod_info, api, retry_delay=300):
    session = api.session
    url = prod_info["url"]

    while True:
        with session.get(url, auth=session.auth, timeout=10) as r:
            status_code = r.status_code

            if status_code == 202:
                logger.info("%s accepted for retrieval", prod_info['title'])
                return prod_info
            elif status_code == 403:
                logger.info("Request for %s exceeded user quota. Retrying in %d seconds",
                        prod_info['title'], retry_delay)
                time.sleep(retry_delay)
            else:
                # Should not happen. As error are processed by _trigger_offline_retrieval
                logger.error("Unexpected response from SciHub")
                raise SentinelAPILTAError("Unexpected response from SciHub")


def trigger_lta(prod_ids, api):
    lta_retry_delay = 600 # try to request a new product from the LTA every 600 seconds

    logger.info(f"Examining {len(prod_ids)} products")

    # download_all will stop as soon as dl_queue is empty.
    # It will not wait for products that were requested from the LTA to become available.
    dl_queue = queue.Queue() # waiting for download

    product_infos = {}
    for prod_id in tqdm(prod_ids, desc="Retrieving product info"):
        product_infos[prod_id] = api.get_product_odata(prod_id)
    
    downloaded_products = {}

    offline_prods = {pid: info for pid, info in product_infos.items() if not info['Online']}
    online_prods = {pid: info for pid, info in product_infos.items() if info['Online']}
    logger.info(f"There are {len(online_prods)} online and {len(offline_prods)} offline products")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_pid = {}

        for prod_id, prod_info in offline_prods.items():
            logger.info('Product %s is in LTA. Putting on retrieval queue.', prod_info['title'])

            future_to_pid[executor.submit(_trigger_lta_inner, prod_info, api)] = prod_id

        for future in concurrent.futures.as_completed(future_to_pid):
            pid = future_to_pid[future]
            prod_info = future.result()

            logger.info(f"Triggered retrieval for product: {prod_info['title']}")

