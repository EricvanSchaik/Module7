from graphs.graph_io import *

with open('examplegraph.gr') as f:
    G = load_graph(f)
with open('mygraph.dot', 'w') as f:
    write_dot(G, f)