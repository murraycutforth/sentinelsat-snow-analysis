#!/bin/bash

# In this script we read a directory path as the first argument to the script, and then we find all .jp2 files inside sentinel data products, and use gdal_translate to convert to tiff.

data_dir=$1
outdir=../data_tif

mkdir $outdir

for base_file in ${data_dir}/*.SAFE
do
	find "$base_file" -name "*.jp2" -exec bash -c 'gdal_translate -of GTiff "$0" "$1/$(basename "$0" .jp2).tif"' {} $outdir \;
done
