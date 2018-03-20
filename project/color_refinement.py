from project.graph_io import *

with open('colorref_smallexample_4_7.grl') as f:
    L = load_graph(f, read_list = True)


def give_isomorphic_pairs(graphs: "list"):
    graph = L[0][0]
    for i in range(1, len(graphs)):
        graph = graph + L[0][i]
    isomorphic_pairs = is_isomorphic(graph)
    if (len(isomorphic_pairs)>0):
        return isomorphic_pairs
    else:
        return "no isomorphic graphs"


def is_isomorphic(graph: "Graph"):
    # A dictionary that maps every vertex to a color
    vertex_color = dict()
    # A dictionary that maps the amount of neighbours to a color
    # Only to be used in the first iteration
    degree_color = dict()
    # The representation of a color
    numbering = 1
    # Give every vertex its initial color in the vertex_color dictionary
    for vertex in graph.vertices:
        if len(vertex.neighbours) not in degree_color:
            degree_color[len(vertex.neighbours)] = numbering
            vertex_color[vertex] = numbering
            numbering += 1
        else:
            vertex_color[vertex] = degree_color[len(vertex.neighbours)]
    # Every iteration of the while loop is an iteration of the color refinement algorithm
    stable = False
    while not stable:
        # A dictionary that maps every color to a combination of neighbouring colors
        color_neighbours = dict()
        stable = True
        # Dict vertices to change color
        vertices_tochange = dict()
        for vertex in graph.vertices:
            # Set neighbourcolors for current vertex
            temp_color_neighbours = dict()
            for neighbour in vertex.neighbours:
                if vertex_color[neighbour] in temp_color_neighbours.keys():
                    temp_color_neighbours[vertex_color[neighbour]] += 1
                else:
                    temp_color_neighbours[vertex_color[neighbour]] = 1
            # If the if-statement is true, the vertex can keep its color, and has to register the colors of its
            # neighbours in the color_neighbours dictionary
            if vertex_color[vertex] not in color_neighbours:
                color_neighbours[vertex_color[vertex]] = temp_color_neighbours
            # Else the vertex has to check if it has the same coloring of neighbours as the original vertex,
            # otherwise give itself a new color
            else:
                if color_neighbours[vertex_color[vertex]] != temp_color_neighbours:
                    vertices_tochange[vertex] = temp_color_neighbours
                    stable = False
        # Change colors of the vertices in vertices tochange
        vertex_changed = []
        for v in vertices_tochange:
            if v not in vertex_changed:
                temp_color_neighbours = vertices_tochange[v]
                vertex_color[v] = numbering
                vertex_changed.append(v)
                for v2 in vertices_tochange:
                    if vertices_tochange[v2] == temp_color_neighbours:
                        vertex_color[v2] = numbering
                        vertex_changed.append(v2)
                numbering += 1

    # Every graph gets its own dict for color and amounts the color appears
    tocompare = dict()
    label = 0
    for i in range(0, len(L[0])):
        color_number = dict()
        for j in range(0, len(L[0][i].vertices)):
            if vertex_color[graph.vertices[label]] in color_number:
                color_number[vertex_color[graph.vertices[label]]] += 1
            else:
                color_number[vertex_color[graph.vertices[label]]] = 1
            label +=1
        tocompare[i] = color_number

    # Now every vertex has its final color, and we have to check if the two graphs are isomorphic
    isomorphic = set()
    for i in range (0, len(tocompare)):
        for j in range (0, len(tocompare)):
            if i != j:
                if tocompare[i] == tocompare[j]:
                    isomorphic.add(frozenset({i, j}))
    return isomorphic

print(give_isomorphic_pairs(L[0]))
