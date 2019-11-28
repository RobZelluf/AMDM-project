import numpy as np
import pandas as pd
import pickle
from utils import read_file, Graph, score_partitioning

filename = 'CA-GrQc.txt'

graph = read_file(filename)


def random_partition(graph, k):
    partitions = np.zeros(graph.num_vertices)
    for vertex in graph.vertices:
        partitions[vertex] = int(np.random.randint(0, k - 1))

    return partitions


partitions = random_partition(graph, 5)
score = score_partitioning(graph, partitions)

print("Score:", score)
