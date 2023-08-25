# Install gdal_translate like this:
#sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
#sudo apt-get update
#sudo apt-get install gdal-bin
#sudo apt-get install libgdal-dev

gdal_translate -of GTiff S2A_MSIL2A_20230726T113321_N0509_R080_T30VVJ_20230726T171500.SAFE/GRANULE/L2A_T30VVJ_A042262_20230726T113322/IMG_DATA/R20m/T30VVJ_20230726T113321_SCL_20m.jp2 test_SCL.tif
gdal_translate -of GTiff S2A_MSIL2A_20230726T113321_N0509_R080_T30VVJ_20230726T171500.SAFE/GRANULE/L2A_T30VVJ_A042262_20230726T113322/IMG_DATA/R10m/T30VVJ_20230726T113321_B03_10m.jp2 test_B03.tif
gdal_translate -of GTiff S2A_MSIL2A_20230726T113321_N0509_R080_T30VVJ_20230726T171500.SAFE/GRANULE/L2A_T30VVJ_A042262_20230726T113322/IMG_DATA/R10m/T30VVJ_20230726T113321_B04_10m.jp2 test_B04.tif
gdal_translate -of GTiff S2A_MSIL2A_20230726T113321_N0509_R080_T30VVJ_20230726T171500.SAFE/GRANULE/L2A_T30VVJ_A042262_20230726T113322/IMG_DATA/R10m/T30VVJ_20230726T113321_B02_10m.jp2 test_B02.tif