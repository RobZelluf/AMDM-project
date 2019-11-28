from utils import read_file, write_file, Graph, score_partitioning
from random_partitioning import random_partition

import numpy as np
import random
import datetime

graph = read_file('ca-GrQc.txt')

partitions = np.zeros(graph.num_vertices)


def one_crawl(graph, v, steps):
    vertices_reached = list()
    for i in range(steps):
        vertices_reached.append(v)
        v = graph.get_connected_vertex(v)
    return vertices_reached


def create_partition(graph, v, steps, crawls):
    partition = list()
    for r in range(crawls):
        crawl = one_crawl(graph, v, steps)
        v = max(set(crawl), key=crawl.count)
        partition.append(v)
    return partition


start = datetime.datetime.now()
#
# init_vertex = 0
# p = partitions[init_vertex]
# while p != 0:
#     init_vertex += 1
#     p = partitions[init_vertex]

partition = create_partition(graph, 0, 100, 100)
print(partition)
print(len(set(partition)))


end = datetime.datetime.now()
print("Crawled in ", (end - start).total_seconds(), "seconds")


# co_visit_matrix =