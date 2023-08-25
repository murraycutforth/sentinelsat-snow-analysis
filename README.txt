**This repo is in early-stage development**

This code is set up to download and analyse Sentinel-2 images for snow coverage. We can use the SCL band in the Level-2A product (which contains a scene classification, including snow/ice and cloud) at 20m and 60m resolution.

The download stage currently runs (which is more complicated than it sounds, uses the ThreadPoolExecutor in Python to request data be made available and then download when it does. For a single tile (covering the Cairngorms) I've found 342 data products (see the ipython notebook for this step), covering the last 6 years. To save memory, only the 20m SCL band is downloaded.

Usage of the main function: run `python -m src.main -h` to see the options.

	usage: main.py [-h] (-D | -A) [--data_dir DATA_DIR] [--geojson_path GEOJSON_PATH] [--download_full]
	
	A program to download and analyse Sentinel-2 data for snowpatch analysis
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -D                    DOWNLOAD mode- run this to cache data
	  -A                    ANALYSIS mode- run this to analyse data after downloading
	
	Args for data download:
	  --data_dir DATA_DIR   Path to dir where data should be cached
	  --geojson_path GEOJSON_PATH
	                        Path to geojson file containing polygons covering all areas which data should be downloaded for
	  --download_full       Store the full tile, rather than cropping to ROI around polygon



TODO
----

 - requirements.txt file
 - Many TODOs littered around the download code
 - Decide on regions which should be measured- currently hardcoded to cairngorms
 - Implement analysis code (such as a probabilistic approach, maybe coupled to ERA-5 reanalysis data so infer snow melt / accumulation in between measurements)
  - Analysis code can use gdal_translate to convert jp2 downloads into tiff, then load into xarray
