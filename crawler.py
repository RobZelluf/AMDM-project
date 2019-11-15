from utils import read_file, write_file, Graph, score_partitioning
import numpy as np
import random
import datetime


graph = read_file()

attached_vertices = dict()
for i in range(graph.num_vertices):
    # attached_vertices[i] = list(np.where(graph.adjacency_matrix[i] == 1))
    attached_vertices[i] = [j for j in range(graph.num_vertices) if graph.adjacency_matrix[i, j] == 1]


def one_crawl(graph, attached_vertices, steps):
    vertices_reached = list()
    index = np.random.randint(0, graph.num_vertices)
    for i in range(steps):
        vertices_reached.append(index)
        index = random.choice(attached_vertices[index])
    return vertices_reached
start = datetime.datetime.now()
one_crawl(graph, attached_vertices, 10000)
end = datetime.datetime.now()
print("Crawled in ", (end - start).total_seconds(), "seconds")
# crawl_visits = np.zeros(1000)

# co_visit_matrix =