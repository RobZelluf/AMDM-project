import numpy as np
import datetime
from collections import defaultdict
from scipy.sparse import lil_matrix
import scipy.sparse as sparse
import random
import networkx as nx


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

        self.adjacency_matrix = lil_matrix((self.num_vertices, self.num_vertices))
        self.build_adjacency_matrix()

        self.laplacian = lil_matrix((self.num_vertices, self.num_vertices))
        self.build_laplacian()

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
        diags = self.adjacency_matrix.sum(axis=1)
        laplacian = sparse.spdiags(diags.flatten(), [0], self.num_vertices, self.num_vertices, format='csr')
        laplacian -= self.adjacency_matrix.copy()
        self.laplacian = laplacian


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
                num_partitions = int(line.split(" ")[4])
                continue

            V = [int(v) for v in line.split()]
            edges.append(V)
            vertices.extend(V)

    vertices = list(set(vertices))
    end = datetime.datetime.now()

    graph = Graph(vertices, edges)

    print("File read in", (end - start).total_seconds(), "seconds")
    print("# vertices:", len(vertices))
    print("# edges:", len(edges))

    return graph, num_partitions


def write_file(filename, graphid, graph, partitioning, num_partitions):
    graphid = graphid[:-4]
    with open('outputs/' + str(filename) + '.output', 'w') as f:
        f.writelines("# " + str(graphid) + " " + str(graph.num_vertices) + " " + str(graph.num_edges) + " " + str(num_partitions) + "\n")
        for vertex in graph.vertices:
            f.writelines("" + str(vertex) + " " + str(partitioning[vertex]) + "\n")
    f.close()


def random_partition(graph, k):
    partitions = np.zeros(graph.num_vertices)
    for vertex in graph.vertices:
        partitions[vertex] = int(np.random.randint(0, k))

    return list(partitions)


def score_partitioning(graph, partitions):
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

    return sum(scores)


def partition_count(partitioning):
    K = max(partitioning) + 1
    counts = [0] * K
    for i in range(len(partitioning)):
        if(partitioning[i] != -1):
            counts[partitioning[i]] += 1
    return counts


def create_nx_graph(filename='CA-GrQc.txt'):
    print(filename)

    graph = nx.Graph()
    vertices = []
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
            vertices.extend(V)
            graph.add_edge(V[0], V[1])

    graph.add_node_from(V)

    return graph

