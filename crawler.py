from utils import read_file, write_file, Graph, score_partitioning
import numpy as np


graph = read_file()

attached_vertices = dict()
for i in range(graph.num_vertices):
    attached_vertices[i] = np.where(graph.adjacency_matrix[i] == 1)

def one_crawl(graph, steps):
    n = graph.num_vertices
    np.random.randint(0,n)
    for i in 1 to N:


crawl_visits = np.zeros(1000)

co_visit_matrix =