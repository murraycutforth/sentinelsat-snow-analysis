from typing import List, Tuple
from pathlib import Path
import logging
import concurrent.futures
import argparse
import time

import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)


def _trigger_lta_inner(prod_info, api, retry_delay=300):
    logger.info(f"Attempting to trigger LTA for {prod_info['title']}")

    session = api.session
    url = prod_info["url"]

    while True:
        with session.get(url, auth=session.auth, timeout=10) as r:
            status_code = r.status_code
            reason = r.reason

        if status_code == 202:
            return prod_info
        elif status_code == 403:
            logger.info("Request for %s exceeded user quota. Retrying in %d seconds", prod_info['title'], retry_delay)
            time.sleep(retry_delay)
        else:
            # Should not happen
            logger.error(f"Unexpected response from SciHub: code {status_code}:{reason}. Retrying in {retry_delay}s.")
            time.sleep(retry_delay)


def trigger_lta(prod_ids, api):
    #lta_retry_delay = 600 # try to request a new product from the LTA every 600 seconds

    logger.info(f"Examining {len(prod_ids)} products")

    product_infos = {}
    for prod_id in tqdm(prod_ids, desc="Retrieving product info"):
        product_infos[prod_id] = api.get_product_odata(prod_id)
    
    downloaded_products = {}

    offline_prods = {pid: info for pid, info in product_infos.items() if not info['Online']}
    online_prods = {pid: info for pid, info in product_infos.items() if info['Online']}
    logger.info(f"There are {len(online_prods)} online and {len(offline_prods)} offline products")

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_to_pid = {}

        # Trigger retrieval for all ofline prods
        for prod_id, prod_info in offline_prods.items():
            future = executor.submit(_trigger_lta_inner, prod_info, api)
            future_to_pid[future] = prod_id

        # As they complete, log a message
        for future in concurrent.futures.as_completed(future_to_pid):
            prod_info = future.result()
            logger.info(f"LTA retrieval request completed for product: {prod_info['title']}")

    logger.info("All offline products triggered for LTA retrieval")

