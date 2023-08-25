from typing import List, Tuple
from dataclasses import dataclass
from math import atan2
from pathlib import Path

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from tqdm import tqdm


def load_test_dataset():

    quantification_factor = 10000  # TODO: confirm that this is correct scale factor

    cache_name = "red_cache.nc"

    if Path(cache_name).exists():
        red_band = xr.open_dataset(cache_name)
    else:
        red_band = xr.open_dataset("test_B04.tif", engine="rasterio").astype(np.float32).coarsen(x=10, boundary="trim").mean().coarsen(y=10, boundary="trim").mean() / quantification_factor
        red_band.to_netcdf(cache_name)

    # Note: to use the rasterio engine, need to also install the rioxarray package: https://corteva.github.io/rioxarray/stable/installation.html
    #green_band = xr.open_dataset("test_B03.tif", engine="rasterio").astype(np.float32).coarsen(x=10, boundary="trim").mean().coarsen(y=10, boundary="trim").mean() / quantification_factor
    #blue_band = xr.open_dataset("test_B02.tif", engine="rasterio").astype(np.float32).coarsen(x=10, boundary="trim").mean().coarsen(y=10, boundary="trim").mean() / quantification_factor
    #scene_mask = xr.open_dataset("test_SCL.tif", engine="rasterio").astype(np.int16).coarsen(x=5, boundary="trim").mean().coarsen(y=5, boundary="trim").mean()
    
    #band_data = [red_band, green_band, blue_band]
    band_data = [red_band]
    
    # Convert the list of data arrays to a single xarray dataset
    data = xr.concat(band_data, dim='band')
    #data['band'] = [0, 1, 2]

    return data





def plot_debug(arr, p):
    fig, axs = plt.subplots(1, 2, figsize=(10,5))

    arr["band_data"].plot(ax=axs[0])
    arr["mask"].plot(ax=axs[1])
    #axs[1].scatter(x=[x[0] for x in p.vertices], y=[x[1] for x in p.vertices])

    plt.show()


def plot(data):
    # See docs for data here: https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l2a/
    
    fig, axs = plt.subplots(2, 2, figsize=(10,10))
    
    axs[0, 0].imshow(data.transpose('y', 'x', 'band').to_array()[0])
    axs[0, 0].set_title('True color')
    
    axs[0, 1].imshow(scene_mask.transpose('y', 'x', 'band').to_array()[0] == 11)
    axs[0, 1].set_title('Snow/Ice mask')
    
    axs[1, 0].imshow((scene_mask.transpose('y', 'x', 'band').to_array()[0] == 9) | (scene_mask.transpose('y', 'x', 'band').to_array()[0] == 8))
    axs[1, 0].set_title('Clouds (medium-high probability)')
    
    axs[1, 1].imshow(scene_mask.transpose('y', 'x', 'band').to_array()[0] == 4)
    axs[1, 1].set_title('Vegetation')
    
    plt.show()


def main():
    dataset = load_test_dataset()

    # Defined in UTM coords, assuming UTM zone is identical to imagery
    northern_corries = Polygon(vertices=[
        (457835.64, 6328955.21),
        (460385.33, 6329486.61),
        (460214.34, 6330601.50),
        (458212.63, 6330287.29),
        ])

    # TODO: temp debug coords, which are much larger
    #northern_corries = Polygon(vertices=[
    #    (437835.64, 6318955.21),
    #    (490385.33, 6319486.61),
    #    (470214.34, 6360601.50),
    #    (438212.63, 6380287.29),
    #    ])


    convex_polygon_mask(northern_corries, dataset)

    print(dataset)

    plot_debug(dataset, northern_corries)



if __name__ == "__main__":
    main()
