from utils import read_file, write_file, Graph, score_partitioning, random_partition

import numpy as np
import random
import datetime

graph = read_file('roadNet-CA.txt')
num_partitions = 100

print(score_partitioning(graph, random_partition(graph, 5)))

def one_crawl(graph, v, steps):
    vertices_reached = list()
    for i in range(steps):
        vertices_reached.append(v)
        v = graph.get_connected_vertex(v)
    return vertices_reached


def init_vertices(graph, init_vert=0):
    visit_count = np.zeros(graph.num_vertices)
    init_verts = list()
    init_verts.append(init_vert)
    for k in range(num_partitions-1):
        print(k+1, "vertices initialized out of ", num_partitions)
        for i in range(10000):
            verts = one_crawl(graph, init_vert, 20)
            for v in verts:
                visit_count[v] += 1
        init_vert = visit_count.argmin()
        init_verts.append(init_vert)
    return init_verts


def assign_partition(graph, partitioning, normalization, assign_v):
    visit_count = np.zeros(graph.num_vertices)
    crawls = int(max(100, 800 - normalization.mean()))
    steps = 20
    if assign_v % int(graph.num_vertices / 100) == 0:
        print("Assigning partition ", assign_v, "out of", graph.num_vertices, "- ", int(assign_v / graph.num_vertices * 100), "%")
        print("Crawls: ", crawls)
        print("Steps: ", steps)
        print("Partition sizes: ", normalization)
    for i in range(crawls):
        verts = one_crawl(graph, assign_v, steps)
        for v in verts:
            visit_count[v] += 1
    # Which partition?
    votes = np.zeros(num_partitions)
    for i in range(len(visit_count)):
        if partitioning[i] != -1:
            votes[partitioning[i]] += visit_count[i]
    if assign_v % int(graph.num_vertices / 100) == 0:
        print(votes)
    normalized_votes = np.divide(votes, normalization)
    return(normalized_votes.argmax())


start = datetime.datetime.now()

init_verts = init_vertices(graph, random.randint(0,graph.num_vertices))

partitioning = np.ones(graph.num_vertices, dtype=int) * -1

for i in range(len(init_verts)):
    partitioning[init_verts[i]] = i

normalization = np.ones(num_partitions)
for i in range(graph.num_vertices):
    if partitioning[i] == -1:
        partitioning[i] = assign_partition(graph, partitioning, normalization, i)
        normalization[partitioning[i]] += 1

end = datetime.datetime.now()

print("Partitioned in ", (end - start).total_seconds(), "seconds")

print(normalization)
print(score_partitioning(graph, partitioning))