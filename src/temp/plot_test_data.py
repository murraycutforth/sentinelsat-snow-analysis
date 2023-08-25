import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# Note: to use the rasterio engine, need to also install the rioxarray package: https://corteva.github.io/rioxarray/stable/installation.html

quantification_factor = 10000  # TODO: confirm that this is correct scale factor
red_band = xr.open_dataset("test_B04.tif", engine="rasterio").astype(np.float32).coarsen(x=10, boundary="trim").mean().coarsen(y=10, boundary="trim").mean() / quantification_factor
green_band = xr.open_dataset("test_B03.tif", engine="rasterio").astype(np.float32).coarsen(x=10, boundary="trim").mean().coarsen(y=10, boundary="trim").mean() / quantification_factor
blue_band = xr.open_dataset("test_B02.tif", engine="rasterio").astype(np.float32).coarsen(x=10, boundary="trim").mean().coarsen(y=10, boundary="trim").mean() / quantification_factor
scene_mask = xr.open_dataset("test_SCL.tif", engine="rasterio").astype(np.int16).coarsen(x=5, boundary="trim").mean().coarsen(y=5, boundary="trim").mean()


band_data = [red_band, green_band, blue_band]


# Convert the list of data arrays to a single xarray dataset
data = xr.concat(band_data, dim='band')
data['band'] = [0, 1, 2]


print(data.max())
print(data.sel(band=0).max())
print(data.sel(band=1).max())
print(data.sel(band=2).max())


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

