**This repo is in early-stage development**

This code is set up to download and analyse Sentinel-2 images for snow coverage. We can use the SCL band in the Level-2A product (which contains a scene classification, including snow/ice and cloud) at 20m and 60m resolution.

The download stage currently runs (which is more complicated than it sounds, uses the ThreadPoolExecutor in Python to request data be made available and then download when it does. For a single tile (covering the Cairngorms) I've found 342 data products (see the ipython notebook for this step), covering the last 6 years. To save memory, only the 20m SCL band is downloaded.

Usage of the main function: run `python -m src.main -h` to see the options.

	usage: main.py [-h] (-D | -A) [--data_dir DATA_DIR] [--geojson_path GEOJSON_PATH] [--download_full] [--api_user API_USER] [--api_password API_PASSWORD]

	A program to download and analyse Sentinel-2 data for snowpatch analysis
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -D                    DOWNLOAD mode- run this to cache data
	  -A                    ANALYSIS mode- run this to analyse data after downloading
	
	Args for data download:
	  --data_dir DATA_DIR   Path to dir where data should be cached
	  --geojson_path GEOJSON_PATH
	                        Path to geojson file containing polygons covering all areas which data should be downloaded for
	  --download_full       Store the full data product, rather than just the 20m SCL band. Uses WAY more disk space.
	  --api_user API_USER   Username for Copernicus Sentinel API
	  --api_password API_PASSWORD
	                        Password for Copernicus Sentinel API



Data Availability
-----------------

See `notebooks/find_available_product_ids.ipynb` for code which explores the number of Sentinel Data products available. This plot shows data for tile 30VVJ, which covers the Cairngorms, showing a reasonable number of data takes for analysis. The level 2A data includes a scene classification, ready to go.

![sentinel_2a_avail](https://github.com/murraycutforth/sentinelsat-snow-analysis/assets/11088372/db7b070f-0a6d-4f35-81b5-0f5a52aa73c5)




TODO
----

 - SCL data before September 2018 isn't being downloaded, probably due to a change in the filename pattern which isn't included in our filter. Investigate.
 - Many TODOs littered around the download code
 - Decide on regions which should be measured- currently hardcoded to cairngorms
 - Implement analysis code (such as a probabilistic approach, maybe coupled to ERA-5 reanalysis data so infer snow melt / accumulation in between measurements)
  - Analysis code can use gdal\_translate to convert jp2 downloads into tiff, then load into xarray
