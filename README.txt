I have got a list of ids for sentinel-2 MSI data

- Improve plot slightly by adding multiple bars for different cloud percentages, with some transparency

Next set up the processing code, we want to iterate over one file at a time
- Trigger LTA (https://sentinelsat.readthedocs.io/en/latest/api_overview.html#lta-products)

My own concurrency codebase is: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor, https://github.com/gbaier/sentinelsat/blob/lta_async/sentinelsat/sentinel.py#L51

- Download required bands into temporary folder - https://github.com/sentinelsat/sentinelsat/blob/f88f1047e4bbc876a275279420bcb48f4966183e/docs/api_overview.rst#L420
- Run gdal_translate to convert from .js2 into .tiff
- Run existing code to load into xarray, get cairngorm mask, and then count the number of snow / cloud
