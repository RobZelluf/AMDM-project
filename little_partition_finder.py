from utils import read_file, write_file, Graph, score_partitioning, random_partition, partition_count
import numpy as np
import datetime
from crawl_utils import *
import pickle

graph = read_file('web-NotreDame.txt')
num_partitions = 20

min_score = 100
final_partitioning = np.zeros(graph.num_vertices, dtype=int)

min_where = -1
for v in range(graph.num_vertices):
    print(v)
    print(min_score)
    partition = list()
    partitioning = np.zeros(graph.num_vertices, dtype=int)
    partitioning[v] = 1
    partition.append(v)
    # search for a one cut
    for i in range(2):
        additions = list()
        for j in range(len(partition)):
            additions += graph.edge_dict[partition[j]]
        partition += list(additions)
        for p in partition:
            partitioning[p] = 1
        score = score_partitioning(graph, partitioning)
        if score < min_score:
            min_score = score
            min_where = v
            final_partitioning = partitioning
            print(score_partitioning(graph, final_partitioning))
        score

print(min_score)
print(min_where)
final_score = score_partitioning(graph, final_partitioning)
print(final_score)

print(np.where(final_partitioning==1))

# write_file('web_', graph, final_partitioning, 2)