from sentinelsat import SentinelAPI

user = "murraycutforth"
password = "6j6xRHZzAu8X"

# Footprint corresponds to cairngorms
# TODO: can we instead just get data for tile 30VVJ, rather than specifiying a polygon of lat/long coordinates?
footprint = "POLYGON ((-3.768020226138653 57.17530811654012,-4.044654037885955 57.02990526013852,-4.1918946151062935 56.874179380367366,-3.7367873764252484 56.81561433549041,-3.5761612921848798 56.68840879227221,-3.214752602644049 56.671252057030955,-2.9113477768566853 56.75695761352293,-2.826572899063158 56.95942257301493,-2.7998018850230966 57.204320271402764,-3.397687865251137 57.33218492834706,-3.768020226138653 57.17530811654012))"

# TODO: make this request much more specific- e.g. limit to specific product/tile/resolution/band?
api = SentinelAPI(user, password)
products = api.query(tileid="30VVJ",
                     platformname="Sentinel-2",
                     cloudcoverpercentage=(0, 30),
                     limit=10)

for i, p in enumerate(products):
    print(i, ".", api.get_product_odata(p), "\n")

print(f"Total of {len(products)} products")

#api.download_all(products)
