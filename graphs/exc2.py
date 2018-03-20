from graphs.graph_io import *
from graphs.graph import *

with open('examplegraph.gr') as f:
    G = load_graph(f)
print("G: "+ str(G))
v = G.vertices[0]
w = G.vertices[3]
G.add_edge(Edge(v, w))
with open('examplegraph2.gr', 'w') as f:
    save_graph(G, f)

H = Graph(G.directed)
vertices = dict()
old_heads = list()
old_tails = list()
for vertex in G.vertices:
    new_vertex = Vertex(H, vertex.label)
    H.add_vertex(new_vertex)
    vertices[vertex] = new_vertex
for edge in G.edges:
    old_heads.append(edge.head.label)
    old_tails.append(edge.tail.label)
for vertex in H.vertices:
    for i in range(len(H.vertices)):
        if vertex != H.vertices[i]:
            if not G.directed and not H.is_adjacent(vertex, H.vertices[i]) and not ((vertex.label in old_tails and old_heads[old_tails.index(vertex.label)] == H.vertices[i].label) or (vertex.label in old_heads and old_tails[old_heads.index(vertex.label)] == H.vertices[i].label)):
                H.add_edge(Edge(vertex, H.vertices[i]))
            elif vertex in old_tails and old_heads[old_tails.index(vertex)] == H.vertices[i]:
                H.add_edge(vertex, H.vertices[i])

print("old edge: " + str(old_tails[0]) + str(old_heads[0]))
with open('complementexamplegraph.gr', 'w') as f:
    save_graph(H, f)