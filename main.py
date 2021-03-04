import holoviews as hv
import numpy as np
import panel as pn
from bokeh.settings import settings

import config
from _util import (
    _return_filename,
    _translate_coords,
    _download_dem,
)

settings.resources = 'cdn'
hv.extension('bokeh')

scalar = 100000
points = hv.Points([(-13193586.0, 4451659.06)]).opts(size=10, min_height=500)
annotator = hv.annotate.instance()
topo = hv.element.tiles.EsriUSATopo().opts(xlim=(-140*scalar, -80*scalar), 
                                           ylim=(30*scalar, 50*scalar),
                                           shared_axes=False,)
layout = annotator(topo * points, name="Point Annotations")
button = pn.widgets.Button(name='Stage DEM for Selected Point')
row = pn.Row()
#gif = pn.pane.GIF('static/sm_earth.gif')
html = pn.pane.HTML("""
    <p>
    Requesting DEM from USGS...
    </p>
    """
)
file_download = pn.widgets.FileDownload(width=380, button_type='primary')

def get_dem(e):
    '''
    
    '''
    row.clear()
    #row.append(gif)
    row.append(html)

    lon, lat = _translate_coords(annotator=annotator, topo=topo)
    
    filename = _return_filename(lon=lon, lat=lat)
    _download_dem(lon=lon, lat=lat)
    
    row.clear()
    file_download.file = f'{config.path}/{config.rawdatdir}/{filename}'
    row.append(file_download)
    
button.on_click(get_dem)

app = pn.Row(
        layout.DynamicMap,
        pn.Column(
            layout.Annotator,
            button,
            row,
        )
    )

app.servable()