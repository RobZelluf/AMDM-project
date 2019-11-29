from utils import read_file, write_file, Graph, score_partitioning

import numpy as np
import random
import datetime

graph = read_file('Oregon-1.txt')

num_partitions = 5
partitioning = np.zeros(graph.num_vertices)
partitioning = partitioning - 1


def one_crawl(graph, v, steps):
    vertices_reached = list()
    for i in range(steps):
        vertices_reached.append(v)
        v = graph.get_connected_vertex(v)
    return vertices_reached


def create_partition(graph, partitioning, v, steps, crawls):
    partition = list()
    for r in range(crawls):
        crawl = one_crawl(graph, v, steps)
        x = max(set(crawl), key=crawl.count)
        if partitioning[x] == -1:
            v = x
            partition.append(v)
    return partition


start = datetime.datetime.now()
#
# init_vertex = 0
# p = partitions[init_vertex]
# while p != 0:
#     init_vertex += 1
#     p = partitions[init_vertex]

for k in range(num_partitions):
    init_vertex = 0
    while partitioning[init_vertex] != -1:
        init_vertex += 1

    partition = create_partition(graph, partitioning, init_vertex, 100, 10000)
    print(partition)
    print(len(set(partition)))
    for v in partition:
        partitioning[v] = k

for v in range(graph.num_vertices):
    if partitioning[v] == -1:
        partitioning[v] = random.randint(0, num_partitions-1)

print(score_partitioning(graph, partitioning))

end = datetime.datetime.now()
print("Crawled in ", (end - start).total_seconds(), "seconds")
