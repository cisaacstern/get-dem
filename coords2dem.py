import os
import sys
import requests

import config
from _util import _return_base_url, _return_filename

def download_file(in_filename, out_filename):
    if not os.path.exists(out_filename):
        print("Downloading", in_filename)
        response = requests.get(in_filename)
        with open(out_filename, 'wb') as f:
            f.write(response.content)
    else:
        print("Skipping download, file already on disk.")

if __name__ == '__main__':
    '''
    Run with, e.g.:
        $ python coords2dem.py 39 119
    '''
    print(sys.argv)
    lat = sys.argv[1]
    lon = sys.argv[2]

    base_url = _return_base_url(lon=lon, lat=lat)
    filename = _return_filename(lon=lon, lat=lat)

    src_url = base_url + filename

    download_file(src_url, f'{config.path}/{config.rawdatdir}/{filename}')