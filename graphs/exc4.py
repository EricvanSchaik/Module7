from graphs.graph import *
from graphs.graph_io import *
import collections

with open('examplegraph.gr') as f:
    G = load_graph(f)


def breadth_first(graph):
    connected = True
    vertices = list()
    vertex = graph.vertices[0]
    distances = collections.OrderedDict()
    distances[vertex] = 0
    vertices.append(vertex)
    j = 1
    while vertices:
        vertex = vertices.pop(0)
        for i in range(len(vertex.neighbours)):
            if vertex.neighbours[i] not in distances.keys():
                vertices.append(vertex.neighbours[i])
                distances[vertex.neighbours[i]] = distances.get(vertex) + 1
                vertex.neighbours[i].label = j
                vertices.append(vertex.neighbours[i])
                j += 1
    for i in graph.vertices:
        if i not in distances:
            connected = False
    distances["Connected"] = connected
    return distances


def depth_first(graph):
    connected = True
    vertices = list()
    vertex = graph.vertices[0]
    distances = collections.OrderedDict()
    distances[vertex] = 0
    vertices.append(vertex)
    j = 1
    while vertices:
        vertex = vertices.pop()
        for i in range(len(vertex.neighbours)):
            if vertex.neighbours[i] not in distances.keys():
                vertices.append(vertex.neighbours[i])
                distances[vertex.neighbours[i]] = distances.get(vertex) + 1
                vertex.neighbours[i].label = j
                vertices.append(vertex.neighbours[i])
                j += 1
            elif distances.get(vertex.neighbours[i]) > distances.get(vertex) + 1:
                distances[vertex.neighbours[i]] = distances.get(vertex) + 1
    for i in graph.vertices:
        if i not in distances:
            connected = False
    distances["Connected"] = connected
    return distances

print(depth_first(G))
with open('mygraph.dot', 'w') as f:
    write_dot(G, f)