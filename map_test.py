from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.models import Circle, HoverTool, MultiLine, Button, Square, InvertedTriangle
from bokeh.models.glyphs import ImageURL
from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import Range1d, Plot
from bokeh.models.graphs import from_networkx
from bokeh.models import ColumnDataSource, Range1d, Plot, LinearAxis, Grid
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
import networkx as nx
import numpy as np
import matplotlib.image as mpimg
from IPython.display import Image
import matplotlib.pyplot as plt

# output to static HTML file
output_file("bokeh_testing.html")

map_options = GMapOptions(lat=30.2861, lng=-97.7394, map_type="roadmap", zoom=11)

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
p = gmap("AIzaSyBqJiQf0gzx86WKwq0a4FVHxwgUIEwAY6Y", map_options, title="Austin")

source = ColumnDataSource(
    data=dict(lat=[ 30.29,  30.20,  30.29],
              lon=[-97.70, -97.74, -97.78])
)

p.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)

show(p)
