from utils import read_file, write_file, Graph, score_partitioning
import numpy as np
import random
import datetime
from random_partitioning import random_partition

graph = read_file()

k = 5
partitioning = random_partition(graph, k)
curr_score = score_partitioning(graph, partitioning)

for i in range(k):
    print("Num", i, " - ", len([x for x in partitioning if x == i]))

vertex = graph.get_random_vertex()
curr_cluster = int(partitioning[vertex])

alpha = 0.1
jumps = 1000
max_cluster_size = (graph.num_vertices - (graph.num_vertices / (k * 2))) / (k - 1)

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

    for i in range(k):
        counts[i] /= partitioning.count(i)

    new_partitioning = graph.num_vertices * [-1]
    random_v = graph.vertices.copy()
    random.shuffle(random_v)
    for v in random_v:
        c_counts = counts[:, v]
        sorted_c = [x for _, x in sorted(zip(c_counts, range(k)))]
        for c in sorted_c:
            if new_partitioning.count(c) < max_cluster_size:
                new_partitioning[v] = c

    new_score = score_partitioning(graph, new_partitioning)
    if new_score < curr_score:
        partitioning = new_partitioning.copy()
        curr_score = new_score
        for i in range(k):
            print("Num", i, " - ", len([x for x in partitioning if x == i]))
        print("---")

    print("Iteration", it, "- Score:", score_partitioning(graph, partitioning))