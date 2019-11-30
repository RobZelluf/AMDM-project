from utils import read_file, write_file, Graph, score_partitioning, random_partition, partition_count
import numpy as np
import datetime
from crawl_utils import *
import pickle

graph = read_file('ca-GrQc.txt')
num_partitions = 2
init_partition_size = 100

partitioning = pickle.load( open( "save.p", "rb" ) )

def seeds_from_partitioning(graph, partitioning, num_partitions):
    seeds = list()
    visit_counts = np.zeros([graph.num_vertices, num_partitions])
    for v in range(graph.num_vertices):
        vertices = one_crawl(graph, v, 3)
        for v in vertices:
            visit_counts[v][partitioning[v]] += 1
    for k in range(num_partitions):
        m = max(visit_counts[:][k])
        seeds.append(np.where(visit_counts[:][k] == m))
    print(seeds)
    return seeds


seeds = seeds_from_partitioning(graph, partitioning, num_partitions)
