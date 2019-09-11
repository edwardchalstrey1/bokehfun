from bokeh.models.graphs import NodesAndLinkedEdges, NodesOnly, EdgesAndLinkedNodes
from bokeh.models import Circle, HoverTool, MultiLine, Button, Square, InvertedTriangle, FreehandDrawTool, PointDrawTool, TapTool, BoxSelectTool
from bokeh.models.glyphs import ImageURL
from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import Range1d, Plot
from bokeh.models.graphs import from_networkx
from bokeh.models import ColumnDataSource, Range1d, Plot, LinearAxis, Grid, LabelSet
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from bokeh.models.annotations import Label
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.palettes import Spectral6
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider
import networkx as nx
import numpy as np
import matplotlib.image as mpimg
from IPython.display import Image
import matplotlib.pyplot as plt
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

defaults = dict(width=400, height=400, padding=0.1)
hv.opts.defaults(
    opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

output_file("bokeh_testing.html")

nodes = [
    {
        "id": 1,
        "type": "Resevoir",
        "edges": [2, 3],
        "demand": [2, 4, 6, 5],
        "pol": [1, 2, 3, 4]
    },
    {
        "id": 2,
        "type": "Tank",
        "edges": [1, 3],
        "demand": [1, 4, 5, 6],
        "pol": [0, 1, 2, 3]
    },
    {
        "id": 3,
        "type": "Junction",
        "edges": [1, 2, 4, 5],
        "demand": [5, 10, 11, 15],
        "pol": [0, 1, 2, 3]
    },
    {
        "id": 4,
        "edges": [3],
        "type": "Tank",
        "demand": [2, 1, 4, 3],
        "pol": [0, 0, 1, 2]
    },
    {
        "id": 5,
        "edges": [3],
        "type": "Tank",
        "demand": [2, 3, 3, 3],
        "pol": [0, 0, 1, 2]
    },
    {
        "id": 6,
        "edges": [5],
        "type": "Tank",
        "demand": [3, 2, 2, 3],
        "pol": [0, 0, 0, 2]
    },
    {
        "id": 7,
        "edges": [6],
        "type": "Tank",
        "demand": [2, 3, 2, 4],
        "pol": [0, 0, 0, 0]
    },
    {
        "id": 8,
        "edges": [7],
        "type": "Tank",
        "demand": [4, 2, 3, 4],
        "pol": [0, 0, 0, 0]
    },
    {
        "id": 9,
        "edges": [6, 3],
        "type": "Junction",
        "demand": [4, 2, 1, 3],
        "pol": [0, 0, 1, 2]
    },
]

def create_network(nodes):
    G = nx.Graph()
    for node in nodes:
        G.add_node(node["id"], node_type=node["type"], demand=node["demand"][0], pol=node["pol"])
        for edge in node["edges"]:
            G.add_edge(node["id"], edge)
    return G

def color_picker(pollution_level):
    if pollution_level == 0:
        return "green"
    elif pollution_level == 1:
        return "yellow"
    elif pollution_level == 2:
        return "orange"
    elif pollution_level == 3:
        return "red"
    else:
        return "black"


graphs = []
for i in range(0,4):
    graph = create_network(nodes)
    node_sizes = []
    node_ids = []
    colors = []
    for node in nodes:
        node_ids.append(node["id"])
        node_sizes.append(node["demand"][i] * 5)
        colors.append(color_picker(node["pol"][i]))
    graphs.append({"graph": graph, "node_ids": node_ids, "node_sizes": node_sizes, "colors": colors})

def draw_network(t):

    # We could use figure here but don't want all the axes and titles
    plot = Plot(x_range=Range1d(-6, 6), y_range=Range1d(-6, 6))

    # Create a Bokeh graph from the NetworkX input using nx.spring_layout
    graph = from_networkx(graphs[t]["graph"], nx.layout.fruchterman_reingold_layout, scale=5, center=(0,0))
    plot.renderers.append(graph)

    graph.node_renderer.data_source.data['colors'] = graphs[t]["colors"]
    graph.node_renderer.data_source.data['sizes'] = graphs[t]["node_sizes"]
    graph.node_renderer.glyph = Circle(size='sizes', fill_color='colors')
    graph.edge_renderer.glyph = MultiLine(line_alpha=1.6, line_width=4)

    # green hover for both nodes and edges
    graph.node_renderer.hover_glyph = Circle(size='sizes', fill_color='#abdda4')
    graph.edge_renderer.hover_glyph = MultiLine(line_color='#abdda4', line_width=8)

    # When we hover over nodes, highlight adjecent edges too
    graph.inspection_policy = NodesAndLinkedEdges()  # can we change this so edges can be hovered over too?

    TOOLTIPS = [
        ("Demand", "@demand"),
        ("Type", "@node_type"),
    ]

    plot.add_tools(HoverTool(tooltips=TOOLTIPS))

    return plot

t = 0
plot = draw_network(0)

# create a callback that will add a number in a random location
def callback():
    global t
    t+=1
    plot = draw_network(t)

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, plot))
