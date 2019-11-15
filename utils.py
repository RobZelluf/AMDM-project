import numpy as np
import datetime


class Graph:
    def __init__(self, vertices, edges):
        self.vertex_map = dict()
        self.vertices = vertices

        self.num_vertices = len(vertices)
        self.num_edges = len(edges)

        self.edges = edges

        self.build_map()
        self.adjacency_matrix = np.zeros((self.num_vertices, self.num_vertices))
        self.build_adjacency_matrix()

    def build_map(self):
        counter = 0
        vertex_map = dict()
        for vertex in self.vertices:
            vertex_map[vertex] = counter
            counter += 1

        self.vertex_map = vertex_map

    def get_vertex_id(self, id):
        return self.vertex_map[id]

    def build_adjacency_matrix(self):
        for edge in self.edges:
            id1 = self.get_vertex_id(edge[0])
            id2 = self.get_vertex_id(edge[1])
            self.adjacency_matrix[id1, id2] = 1


def read_file(filename='CA-GrQc.txt'):
    vertices = []
    edges = []

    start = datetime.datetime.now()
    with open('data/' + filename, 'r') as f:
        for line in f.readlines():
            if line[0] == "#" or line[0] == " ":
                continue

            V = [int(v) for v in line.split()]
            edges.append(V)
            for vertex in V:
                if vertex not in vertices:
                    vertices.append(vertex)

    end = datetime.datetime.now()

    print("File read in", (end - start).total_seconds(), "seconds")
    print("# vertices:", len(vertices))
    print("# edges:", len(edges))

    graph = Graph(vertices, edges)
    return graph


def write_file(graphid, graph, partitions):
    with open('data/' + str(graphid) + '.output', 'w') as f:
        f.writelines("# " + str(graphid) + " " + str(graph.num_vertices) + " " + str(graph.num_edges) + "\n")
        for vertex in graph.vertices:
            f.writelines("" + str(vertex) + " " + str(partitions[graph.vertex_map[vertex]]) + "\n")
    f.close()


def score_partitioning(graph, partitions):
    start = datetime.datetime.now()
    scores = np.zeros(int(max(partitions) + 1))
    for edge in graph.edges:
        id1 = graph.get_vertex_id(edge[0])
        id2 = graph.get_vertex_id(edge[1])

        cluster1 = int(partitions[id1])
        cluster2 = int(partitions[id2])

        if cluster1 != cluster2:
            scores[cluster1] += 1
            scores[cluster2] += 1

    for i in range(len(scores)):
        scores[i] /= len([x for x in partitions if x == i])

    end = datetime.datetime.now()
    print("Score calculated in", (end-start).total_seconds(), "seconds")
    return sum(scores)


def get_laplacian(adjacency_matrix):
    laplacian = -adjacency_matrix
    for j in range(len(adjacency_matrix)):
        laplacian[j][j] = sum(adjacency_matrix[j]) # diagonal entries are degree of vertex

    return laplacian