import numpy as np


def random_partition(graph, k):
    partitions = np.zeros(graph.num_vertices)
    for vertex in graph.vertices:
        partitions[vertex] = int(np.random.randint(0, k))

    return list(partitions)
