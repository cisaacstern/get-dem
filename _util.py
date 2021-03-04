import subprocess

import numpy as np

import config

def _return_base_url(lon, lat):
    '''

    '''
    base = 'https://prd-tnm.s3.amazonaws.com/StagedProducts'
    modifier = f'/Elevation/1/TIFF/n{lat}w{lon}/'
    return base + modifier

def _return_filename(lon, lat):
    '''

    '''
    return f'USGS_1_n{lat}w{lon}.tif'

def _translate_coords(annotator, topo):
    '''
    Parameters
    ==========
    annotator : hv.annotate.instance()

    topo : hv.Tiles object
        
    '''
    df = annotator.annotated.dframe()
    easting = df['x'][0]
    northing = df['y'][0]

    lon, lat = topo.easting_northing_to_lon_lat(easting, northing)

    lon = int(np.abs(np.floor(lon)))
    lat = int(np.ceil(lat))
    return lon, lat

def _download_dem(lon, lat):
    '''

    '''
    subprocess.run(['python', f'{config.path}/coords2dem.py', f'{lat}', f'{lon}'])

def _subset_transform(dataset):
    '''

    '''
    x0_o, y0_o = dataset.transform * (0, 0)
    res = (dataset.bounds.right - dataset.bounds.left) / dataset.shape[0]
    
    return Affine.translation(x0_s, y0_s) * Affine.scale(res, res)

def _subset_raster(lon, lat):
    '''
    Creates a 300 x 300 cell bounding box centered on selected point
    '''
    basefn = _return_filename(lon=lon, lat=lat)
    basepath = f'{config.rawdatdir}/{basefn}'
    print(f'Subsetting this file: {basepath}')

    dataset, arr, res, _ = _open(config.rawdatdir, basefn)

    subset_fn = basefn.replace('.tif', f'subset_n{lat}w{lon}.tif')
    subset_arr = arr[nrows:nrows+extent, ncols:ncols+extent]
    
    transform = Affine.translation(x0_s, y0_s) * Affine.scale(res, res)


    with rasterio.open(
        f'{config.subsetdir}/{subsetfn}',
        'w',
        driver='GTiff',
        height=inset.shape[0],
        width=inset.shape[1],
        count=1,
        dtype=inset.dtype,
        crs=dataset.meta['crs'],
        transform=transform,
    ) as dst:
        dst.write(subset, 1)
    # return subset_filename, 

