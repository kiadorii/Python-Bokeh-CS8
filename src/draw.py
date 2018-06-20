import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval, LabelSet, Label
from bokeh.palettes import Spectral8

from graph import *

graph_data = Graph()
graph_data.debug_create_test_data()

N = len(graph_data.vertexes)
node_indices = list(range(N))

# debug_pallete = Spectral8
# debug_pallete.append('#ff0000')
# debug_pallete.append('#0000ff')
color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, 500), y_range=(0, 500),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Oval(height=20, width=25, fill_color='color')

# this is drawing the edges from start to end

graph.edge_renderer.data_source.data = dict(
    start=[0]*N, # this is a list of some kind that has to do with starting points
    end=node_indices) # this is a list of some kind thathas to do with ending points

### start of layout code
# Looks like this is setting the positions of the vertexes
# circ = [i*2*math.pi/8 for i in node_indices] # - we don't want a circle
# x = [math.cos(i) for i in circ] # This is assembling a list for us
# y = [math.sin(i) for i in circ]
val = [v.value[::] for v in graph_data.vertexes]
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]
# vertex_name = [v.name['a'] for names in graph_data.vertexes]
print(val)

# source = ColumnDataSource(data=dict(x, y, graph_data.debug_create_test_data))
# labels = LabelSet(x='weight', y='height', text='names', level='glyph',
#               x_offset=5, y_offset=5, source=source, render_mode='canvas')
graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

output_file('graph.html')
show(plot)