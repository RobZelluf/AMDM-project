from utils import read_file, write_file, Graph, score_partitioning
import numpy as np
import random
import datetime

graph = read_file('ca-GrQc.txt')

def one_crawl(graph, steps):
    vertices_reached = list()
    index = np.random.randint(0, graph.num_vertices)
    for i in range(steps):
        vertices_reached.append(index)
        index = graph.get_connected_vertex(index)
    x = max(set(vertices_reached), key=vertices_reached.count)
    return vertices_reached


def many_crawls(graph, steps, crawls):
    co_visit_matrix = np.zeros((graph.num_vertices, graph.num_vertices))
    for r in range(crawls):
        vertices_reached = one_crawl(graph, steps)
        for i in range(len(vertices_reached)):
            for j in range(i+1, len(vertices_reached)):
                if vertices_reached[i] != vertices_reached[j]:
                    co_visit_matrix[vertices_reached[i]][vertices_reached[j]] += 1
                    co_visit_matrix[vertices_reached[j]][vertices_reached[i]] += 1
    return co_visit_matrix


start = datetime.datetime.now()
co_visit_matrix = many_crawls(graph, 100, 1000)
print(co_visit_matrix[0, :])
end = datetime.datetime.now()
print("Crawled in ", (end - start).total_seconds(), "seconds")


# co_visit_matrix =