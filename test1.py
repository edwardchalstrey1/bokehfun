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

G = nx.gnm_random_graph(15, 30)

# We could use figure here but don't want all the axes and titles
plot = Plot(x_range=Range1d(-2, 2), y_range=Range1d(-2 ,2))

# Create a Bokeh graph from the NetworkX input using nx.spring_layout
graph = from_networkx(G, nx.spring_layout, scale=1.8, center=(0,0))
plot.renderers.append(graph)

# Blue circles for nodes, and light grey lines for edges
graph.node_renderer.glyph = Circle(size=25, fill_color='#2b83ba')
graph.edge_renderer.glyph = MultiLine(line_color="#cccccc", line_alpha=0.8, line_width=2)

# green hover for both nodes and edges
graph.node_renderer.hover_glyph = Circle(size=25, fill_color='#abdda4')
graph.edge_renderer.hover_glyph = MultiLine(line_color='#abdda4', line_width=4)

# When we hover over nodes, highlight adjecent edges too
graph.inspection_policy = NodesAndLinkedEdges()

plot.add_tools(HoverTool(tooltips=None))

show(plot)
