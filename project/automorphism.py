from project.graph_io import *

with open('torus24.grl') as f:
    L = load_graph(f, read_list=True)


def amount_of_automorphisms(graphs: "list", i: "int"):
    graph = graphs[i]
    color_number, vertex_color, numbering = refine_color1(graph)
    lowest_duplicate_color = None
    number_of_automorphisms = int(0)
    for color in color_number.keys():
        if color_number[color] > 1 and not lowest_duplicate_color:
            lowest_duplicate_color = color
        elif 1 < color_number[color] < color_number[lowest_duplicate_color]:
            lowest_duplicate_color = color
    if not lowest_duplicate_color:
        return 1
    else:
        currentcolor_vertices = list()
        for vertex in vertex_color.keys():
            if vertex_color[vertex] == lowest_duplicate_color:
                currentcolor_vertices.append(vertex)
        graphN = graph
        graphN = graphN + graph
        vertex_colorN = dict()
        L = len(graph.vertices)
        for i in range(len(graph.vertices)):
            vertex_colorN[graphN.vertices[i]] = vertex_color[graph.vertices[i]]
            vertex_colorN[graphN.vertices[i + L]] = vertex_color[graph.vertices[i]]
        currentvertex = currentcolor_vertices[0]
        for vertex in currentcolor_vertices:
            vertex_colorN[graphN.vertices[graph.vertices.index(currentvertex)]] = numbering
            vertex_colorN[graphN.vertices[graph.vertices.index(vertex) + L]] = numbering
            number_of_automorphisms = treebranch(graphN, vertex_colorN.copy(), numbering, number_of_automorphisms)
            vertex_colorN[graphN.vertices[graph.vertices.index(vertex) + L]] = lowest_duplicate_color
        return number_of_automorphisms


def refine_color1(graph: "Graph"):
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
    label = 0
    color_number = dict()
    for j in range(0, len(L[0][0].vertices)):
        if vertex_color[graph.vertices[label]] in color_number:
            color_number[vertex_color[graph.vertices[label]]] += 1
        else:
            color_number[vertex_color[graph.vertices[label]]] = 1
        label += 1
    return color_number, vertex_color, numbering


def refine_color2(graphN, vertex_colorN, numbering):
    stable = False
    while not stable:
        # A dictionary that maps every color to a combination of neighbouring colors
        color_neighbours = dict()
        stable = True
        # Dict vertices to change color
        vertices_tochange = dict()
        for vertex in graphN.vertices:
            # Set neighbourcolors for current vertex
            temp_color_neighbours = dict()
            for neighbour in vertex.neighbours:
                if vertex_colorN[neighbour] in temp_color_neighbours.keys():
                    temp_color_neighbours[vertex_colorN[neighbour]] += 1
                else:
                    temp_color_neighbours[vertex_colorN[neighbour]] = 1
            # If the if-statement is true, the vertex can keep its color, and has to register the colors of its
            # neighbours in the color_neighbours dictionary
            if vertex_colorN[vertex] not in color_neighbours:
                color_neighbours[vertex_colorN[vertex]] = temp_color_neighbours
            # Else the vertex has to check if it has the same coloring of neighbours as the original vertex,
            # otherwise give itself a new color
            else:
                if color_neighbours[vertex_colorN[vertex]] != temp_color_neighbours:
                    vertices_tochange[vertex] = temp_color_neighbours
                    stable = False
        # Change colors of the vertices in vertices tochange
        vertex_changed = []
        for v in vertices_tochange:
            if v not in vertex_changed:
                temp_color_neighbours = vertices_tochange[v]
                vertex_colorN[v] = numbering
                vertex_changed.append(v)
                for v2 in vertices_tochange:
                    if vertices_tochange[v2] == temp_color_neighbours:
                        vertex_colorN[v2] = numbering
                        vertex_changed.append(v2)
                numbering += 1
    return vertex_colorN, numbering


def treebranch(graphN, vertex_colorN, numbering, number_of_automorphisms):
    numbering += 1
    vertex_colorN, numbering = refine_color2(graphN, vertex_colorN, numbering)
    color_number1 = dict()
    color_number2 = dict()
    for color in vertex_colorN.values():
        color_number1[color] = 0
        color_number2[color] = 0
    for vertex in graphN.vertices:
        if graphN.vertices.index(vertex) < len(graphN.vertices) // 2:
            color_number1[vertex_colorN[vertex]] += 1
        else:
            color_number2[vertex_colorN[vertex]] += 1
    if not_isomorphic(color_number1, color_number2):
        print("niet isomorph")
        return number_of_automorphisms
    else:
        lowest_duplicate_color = lowest_duplicate(color_number1)
        if not lowest_duplicate_color:
            number_of_automorphisms += 1
            print("automorph")
            return number_of_automorphisms
        else:
            currentcolor_vertices = list()
            for i in range(len(graphN.vertices)):
                if vertex_colorN[graphN.vertices[i]] == lowest_duplicate_color:
                    currentcolor_vertices.append(graphN.vertices[i])
            vertex1 = currentcolor_vertices[0]
            print("vertex1:", vertex1)
            for i in range(len(currentcolor_vertices) // 2):
                vertex_colorN[vertex1] = numbering
                vertex_colorN[graphN.vertices[graphN.vertices.index(currentcolor_vertices[i+len(currentcolor_vertices)//2])]] = numbering
                print("vertex2:", graphN.vertices[graphN.vertices.index(currentcolor_vertices[i+len(currentcolor_vertices)//2])])
                x = treebranch(graphN, vertex_colorN.copy(), numbering, number_of_automorphisms)
                number_of_automorphisms = x
                vertex_colorN[vertex1] = lowest_duplicate_color
                vertex_colorN[graphN.vertices[graphN.vertices.index(currentcolor_vertices[i]) + len(graphN.vertices) // 2]] = lowest_duplicate_color
            return number_of_automorphisms


def not_isomorphic(color_number1, color_number2):
    return color_number1 != color_number2


def lowest_duplicate(color_number: "dict"):
    lowest_duplicate_color = None
    for color in color_number.keys():
        if color_number[color] > 1 and not lowest_duplicate_color:
            lowest_duplicate_color = color
        elif color_number[color] > 1 and color_number[color] < color_number[lowest_duplicate_color]:
            lowest_duplicate_color = color
    return lowest_duplicate_color


print(amount_of_automorphisms(L[0], 0))
