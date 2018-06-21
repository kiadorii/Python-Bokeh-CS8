import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, ColumnDataSource, Range1d, LabelSet, Label
from bokeh.palettes import Spectral8

from graph import *

WIDTH = 500
HEIGHT = 500 # TODO: Currently graph renders square to these numbers
CIRCLE_SIZE = 30

graph_data = Graph()
graph_data.debug_create_test_data()
graph_data.bfs(graph_data.vertexes[0])

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Circle(size=CIRCLE_SIZE, fill_color='color')

# this is drawing the edges from start to end
# This retrieves the vertexes dynamically (rather than static)
start_indexes = []
end_indexes = []

for start_index, vertex in enumerate(graph_data.vertexes): # use enumerate to get the indexes
    for e in vertex.edges:
        start_indexes.append(start_index)
        end_indexes.append(graph_data.vertexes.index(e.destination))

graph.edge_renderer.data_source.data = dict(
    start=start_indexes,
    end=end_indexes
)

# Static form
# graph.edge_renderer.data_source.data = dict(
#     start=[0]*N, # a list if vertex indexes to start edges from
#     end=node_indices) # a list of vertex index to end edges at

# Start of layout code
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

# Create a new dictionary to use as a data source, with three lists in it, ordered in the same way as vertexes
# List of x values 
# List of y values
# List of labels
value = [v.value for v in graph_data.vertexes] # Possible optimization: We run through this loop three times
label_source = ColumnDataSource(data=dict(x = x, y = y, v = value))

labels = LabelSet(x='x', y='y', text='v', level='glyph', 
    source=label_source, render_mode='canvas', text_align='center', text_baseline='middle')

# TODO: Investigate plot.add_layout vs. plot.renderers.append
plot.add_layout(labels)

output_file('graph.html')
show(plot)