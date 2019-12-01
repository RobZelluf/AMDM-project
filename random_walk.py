from utils import read_file, write_file, Graph, score_partitioning
import numpy as np
from time import sleep
import random
import datetime
from random_partitioning import random_partition
import pickle as p

graph = read_file()
k = 5

walk_length = 1
iterations = 100

partition = [[v] for v in graph.vertices]

for it in range(iterations):
    total_visits = []
    for i in range(len(partition)):
        c = partition[i]
        vertex = random.sample(c, 1)[0]
        visits = c.copy()
        for walk in range(walk_length):
            vertex = graph.get_connected_vertex(vertex)
            visits.append(vertex)

        total_visits.append(visits)

    total_clusters = []
    for v in graph.vertices:
        clusters = [c for c in total_visits if v in c]
        total_clusters.append(clusters)

    # total_clusters = sorted(total_clusters, key=len, reverse=True)

    new_partition = []
    vertices_merged = []
    i = 0
    for cluster in total_clusters:
        all_vertices = list(set([y for x in cluster for y in x]))
        merge = True
        for v in all_vertices:
            if v in vertices_merged:
                merge = False
                break

        if merge:
            new_partition.append(all_vertices)
            vertices_merged.extend(all_vertices)

    for cluster in partition:
        merge = True
        for v in cluster:
            if v in vertices_merged:
                merge = False
                break

        if merge:
            new_partition.append(cluster)
            vertices_merged.extend(cluster)

    for v in graph.vertices:
        if v not in vertices_merged:
            new_partition.append([v])

    print(new_partition)
    print(len(new_partition))

    hanlo = []
    for clus in new_partition:
        hanlo.extend(clus)

    print(len(list(set(hanlo))))
    partition = new_partition.copy()


