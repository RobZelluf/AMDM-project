import numpy as np
import pandas as pd
import pickle
from utils import read_file, Graph, score_partitioning


def random_partition(graph, k):
    partitions = np.zeros(graph.num_vertices)
    for vertex in graph.vertices:
        partitions[vertex] = int(np.random.randint(0, k))

    return list(partitions)
