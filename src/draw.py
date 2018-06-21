import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval, ColumnDataSource, RangeId, LabelSet, Label
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
# This retrieves the vertexes dynamically (rather than static)
start_indexes = []
end_indexes = []

for start_indexes, vertex in enumerate(graph_data.vertexes): # use enumerate to get the indexes
    for e in vertex.edges:
        start_indexes.append(start_indexes)
        end_indexes.append(graph_data.vertexes.index(e.destination))

graph.edge_renderer.data_source.data = dict(
    start=start_indexes,
    end=end_indexes
)

# Static form
# graph.edge_renderer.data_source.data = dict(
#     start=[0]*N, # a list if vertex indexes to start edges from
#     end=node_indices) # a list of vertex index to end edges at

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


source = ColumnDataSource(data=dict(height=[66, 71, 72, 68, 58, 62],
                                    weight=[165, 189, 220, 141, 260, 174],
                                    names=['Mark', 'Amir', 'Matt', 'Greg',
                                           'Owen', 'Juan']))


labels = LabelSet(x='weight', y='height', text='names', level='glyph',
              x_offset=5, y_offset=5, source=source, render_mode='canvas')

citation = Label(x=70, y=70, x_units='screen', y_units='screen',
                 text='Collected by Luke C. 2016-04-01', render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)

plot.add_layout(labels)
plot.add_layout(citation)

output_file('graph.html')
show(plot)