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
        try:
            self.adjacency_matrix = np.zeros((self.num_vertices, self.num_vertices))
            self.laplacian = np.zeros((self.num_vertices, self.num_vertices))
            self.attached_vertices = dict()
            self.build_adjacency_matrix()
            self.build_laplacian()
            self.build_attached_vertices()

            for i in range(self.num_vertices):
                assert sum(self.laplacian[i]) == 0

        except:
            print("Too much data to build matrices!!")

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
            self.adjacency_matrix[id2, id1] = 1

    def build_laplacian(self):
        laplacian = self.adjacency_matrix.copy()
        for j in range(self.num_vertices):
            laplacian[j][j] = sum(self.adjacency_matrix[j, :])  # diagonal entries are degree of vertex

    def build_attached_vertices(self):
        for i in range(self.num_vertices):
            # attached_vertices[i] = list(np.where(graph.adjacency_matrix[i] == 1))
            self.attached_vertices[i] = [j for j in range(self.num_vertices) if self.adjacency_matrix[i, j] == 1]


def read_file(filename='CA-GrQc.txt'):
    print(filename)
    vertices = []
    edges = []

    start = datetime.datetime.now()
    with open('data/' + filename, 'r') as f:
        i = 0
        lines = f.readlines()
        for line in lines:
            if i % 10000 == 0:
                print("Reading line", i, "out of", len(lines), "- ", int(i / len(lines) * 100), "%")

            i += 1

            if line[0] == "#" or line[0] == " ":
                continue

            V = [int(v) for v in line.split()]
            edges.append(V)
            for vertex in V:
                vertices.append(vertex)

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
    print("Score calculated in", (end - start).total_seconds(), "seconds")
    return sum(scores)
