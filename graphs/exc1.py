from graphs.graph import *


def create_graph_wpath(n):
    graph = Graph(False, n)
    for i in range(n - 1):
        graph.add_edge(Edge(graph.vertices[i], graph.vertices[i + 1]))
    print(len(graph.vertices))
    return graph


def create_graph_wcycle(n):
    graph = Graph(False, n)
    for i in range(n):
        if i + 1 == len(graph.vertices):
            graph.add_edge(Edge(graph.vertices[i], graph.vertices[0]))
        else:
            graph.add_edge(Edge(graph.vertices[i], graph.vertices[i + 1]))
    return graph


def create_complete_graph(n):
    graph = Graph(False, n)
    for i in range(n):
        for j in range(n):
            if graph.vertices[j] != graph.vertices[i]:
                graph.add_edge(Edge(graph.vertices[i], graph.vertices[j]))
    return graph

