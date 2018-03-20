from project.graph_io import *
from collections import Counter

with open('cubes6.grl') as f:
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
    # Create variables
    vertex_color = dict()
    degree_color = dict()
    numbering = 1

    # Give every vertex its initial color in the vertex_color dictionary
    for vertex in graph.vertices:
        if len(vertex.neighbours) not in degree_color:
            degree_color[len(vertex.neighbours)] = numbering
            vertex_color[vertex] = numbering
            numbering += 1
        else:
            vertex_color[vertex] = degree_color[len(vertex.neighbours)]

    # Give new colors till graph is stable
    vertex_color, numbering = give_colors(vertex_color, numbering, graph)

    # Every graph gets its own dict for color and amounts the color appears
    tocompare = dict()
    label = 0
    labelstart = []
    for i in range(0, len(L[0])):
        labelstart.append(label)
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
    for i in range(0, len(tocompare)):
        for j in range(0, len(tocompare)):
            if i != j:
                if {i, j} not in isomorphic:
                    if isomorphicgraphs(tocompare, i, j, labelstart, vertex_color, numbering, graph):
                        ij={i,j}
                        isomorphic.add(frozenset(ij))
    return isomorphic


def isomorphicgraphs(tocompare, i, j, labelstart, vertex_color, numbering, graph):
    if tocompare[i] == tocompare[j]:
            #branching
            if Counter(tocompare[i].values())[1] < len(tocompare[i]):
                #make graph with only the graphs to branch
                branchgraph = L[0][i] + L[0][j]
                branchcolor = dict()
                label = labelstart[i]
                x = 0
                for vertex in branchgraph:
                    if x >= len(L[0][i].vertices):
                        label = labelstart[j]
                        x = -i*j
                    branchcolor[vertex] = vertex_color[graph.vertices[label]]
                    label += 1
                    x += 1
                #what is the double color
                color = -1
                for key in tocompare[i].keys():
                    if tocompare[i][key]>1:
                        color = key
                        break
                #change color of 1 graph
                currentkey = ""
                for key in branchcolor.keys():
                    if key.label < len(L[0][i].vertices):
                        if branchcolor[key] == color:
                            currentkey = key
                            break
                changedcolor = numbering
                numbering += 1
                branchcolor[currentkey] = changedcolor
                currentkey = ""

                #check if isomorph
                usedkeys = []
                isomorph = False
                while not isomorph:
                    if currentkey:
                        branchcolor[currentkey] = color
                        currentkey = ""
                    for key in branchcolor.keys():
                        if key.label >= len(L[0][i].vertices):
                            if branchcolor[key] == color and key not in usedkeys:
                                usedkeys.append(key)
                                currentkey = key
                                break
                    if not currentkey:
                        return False
                    else:
                        branchcolor[currentkey] = changedcolor
                        branchcolorattempt, numberingattempt = give_colors(branchcolor, numbering, branchgraph)
                        branchcompare = dict()
                        label = 0
                        color_number = dict()
                        for x in range(0, len(L[0][i].vertices)):
                            if branchcolorattempt[branchgraph.vertices[label]] in color_number:
                                color_number[branchcolorattempt[branchgraph.vertices[label]]] += 1
                            else:
                                color_number[branchcolorattempt[branchgraph.vertices[label]]] = 1
                            label += 1
                        branchcompare[i] = color_number
                        color_number = dict()
                        for x in range(len(L[0][i].vertices), len(L[0][i].vertices)+len(L[0][j].vertices)):
                            if branchcolorattempt[branchgraph.vertices[label]] in color_number:
                                color_number[branchcolorattempt[branchgraph.vertices[label]]] += 1
                            else:
                                color_number[branchcolorattempt[branchgraph.vertices[label]]] = 1
                            label += 1
                        branchcompare[j] = color_number
                        startlabel = [None]*(1+max(i,j))
                        startlabel[i]=0
                        startlabel[j]=len(L[0][i].vertices)
                        if isomorphicgraphs(branchcompare,i,j,startlabel,branchcolorattempt,numbering,branchgraph):
                            isomorph = True
                            return True
            else:
                return True
    return False

def give_colors(vertex_color, numbering, graph):
    # Every iteration of the while loop is an iteration of the color refinement algorithm
    stable = False
    vertex_color2 = vertex_color.copy()
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
                if vertex_color2[neighbour] in temp_color_neighbours.keys():
                    temp_color_neighbours[vertex_color2[neighbour]] += 1
                else:
                    temp_color_neighbours[vertex_color2[neighbour]] = 1
            # If the if-statement is true, the vertex can keep its color, and has to register the colors of its
            # neighbours in the color_neighbours dictionary
            if vertex_color2[vertex] not in color_neighbours:
                color_neighbours[vertex_color2[vertex]] = temp_color_neighbours
            # Else the vertex has to check if it has the same coloring of neighbours as the original vertex,
            # otherwise give itself a new color
            else:
                if color_neighbours[vertex_color2[vertex]] != temp_color_neighbours:
                    vertices_tochange[vertex] = temp_color_neighbours
                    stable = False
        # Change colors of the vertices in vertices tochange
        vertex_changed = []
        for v in vertices_tochange:
            if v not in vertex_changed:
                temp_color_neighbours = vertices_tochange[v]
                vertex_color2[v] = numbering
                vertex_changed.append(v)
                for v2 in vertices_tochange:
                    if vertices_tochange[v2] == temp_color_neighbours:
                        vertex_color2[v2] = numbering
                        vertex_changed.append(v2)
                numbering += 1
    return vertex_color2 ,numbering

print(give_isomorphic_pairs(L[0]))
