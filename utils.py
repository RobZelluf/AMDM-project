import numpy as np
import datetime
from collections import defaultdict
import random


class Graph:
    def __init__(self, vertices, edges):
        self.vertex_map = dict()
        self.vertices = vertices

        self.num_vertices = len(vertices)
        self.num_edges = len(edges)

        self.edges = edges
        self.build_map()
        self.edge_dict = defaultdict(list)
        self.build_edge_dict()

        # try:
        #     self.adjacency_matrix = np.zeros((self.num_vertices, self.num_vertices))
        #     self.laplacian = np.zeros((self.num_vertices, self.num_vertices))
        #     self.build_adjacency_matrix()
        #     self.build_laplacian()
        #
        #     for i in range(self.num_vertices):
        #         assert sum(self.laplacian[i]) == 0
        #
        # except:
        #     print("Too much data to build matrices!!")

    def build_map(self):
        counter = 0
        vertex_map = dict()
        for vertex in self.vertices:
            vertex_map[vertex] = counter
            counter += 1

        self.vertex_map = vertex_map

    def build_edge_dict(self):
        for edge in self.edges:
            self.edge_dict[edge[0]].append(edge[1])
            self.edge_dict[edge[1]].append(edge[0])

    def get_connected_vertex(self, v):
        return random.sample(self.edge_dict[v], 1)[0]

    def get_random_vertex(self):
        return random.sample(self.vertices, 1)[0]

    def check_edge(self, v1, v2):
        if [v1, v2] in self.edges or [v2, v1] in self.edges:
            return True
        else:
            return False

    def build_adjacency_matrix(self):
        for edge in self.edges:
            id1 = edge[0]
            id2 = edge[1]
            self.adjacency_matrix[id1, id2] = 1
            self.adjacency_matrix[id2, id1] = 1

    def build_laplacian(self):
        laplacian = self.adjacency_matrix.copy()
        for j in range(self.num_vertices):
            laplacian[j][j] = sum(self.adjacency_matrix[j, :])  # diagonal entries are degree of vertex


def read_file(filename='CA-GrQc.txt'):
    print(filename)
    vertices = []
    edges = []

    start = datetime.datetime.now()
    with open('data/' + filename, 'r') as f:
        i = 0
        lines = f.readlines()
        for line in lines:
            if i % int(len(lines) / 10) == 0:
                print("Reading line", i, "out of", len(lines), "- ", int(i / len(lines) * 100), "%")

            i += 1

            if line[0] == "#" or line[0] == " ":
                continue

            V = [int(v) for v in line.split()]
            edges.append(V)
            vertices.extend(V)

    vertices = list(set(vertices))
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
        id1 = edge[0]
        id2 = edge[1]

        cluster1 = int(partitions[id1])
        cluster2 = int(partitions[id2])

        if cluster1 != cluster2:
            scores[cluster1] += 1
            scores[cluster2] += 1

    for i in range(len(scores)):
        scores[i] /= len([x for x in partitions if x == i])

    end = datetime.datetime.now()
    print("Score calculated in", (end - start).total_seconds(), "seconds")
    return sum(scores)
