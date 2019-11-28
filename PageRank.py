from utils import read_file, write_file, Graph, score_partitioning
import numpy as np
import random
import datetime
from random_partitioning import random_partition

graph = read_file()

k = 5
partitioning = random_partition(graph, k)

for i in range(k):
    print("Num", i, " - ", len([x for x in partitioning if x == i]))

vertex = graph.get_random_vertex()
curr_cluster = int(partitioning[vertex])

alpha = 0.001
jumps = 1000
max_cluster_size = graph.num_vertices / (k * 0.8)

iterations = 100

for it in range(iterations):
    counts = np.zeros((k, graph.num_vertices))
    jump = 0
    while jump < jumps:
        if random.random() > alpha:
            vertex = graph.get_connected_vertex(vertex)
            counts[curr_cluster][vertex] += 1
        else:
            jump += 1
            vertex = graph.get_random_vertex()
            curr_cluster = int(partitioning[vertex])

    for v in graph.vertices:
        c_counts = counts[:, v]
        sorted_c = [x for _, x in sorted(zip(c_counts, range(k)))]
        for c in sorted_c:
            if partitioning.count(c) < max_cluster_size:
                partitioning[v] = c

    print("Iteration", it, "- Score:", score_partitioning(graph, partitioning))
    for i in range(k):
        print("Num", i, " - ", len([x for x in partitioning if x == i]))
    print("---")