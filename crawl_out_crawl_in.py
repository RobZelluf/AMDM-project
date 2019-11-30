from utils import read_file, write_file, Graph, score_partitioning, random_partition

import numpy as np
import random
import datetime

graph = read_file('ca-GrQc.txt')
num_partitions = 2

print("Random Partition Score: ", score_partitioning(graph, random_partition(graph, num_partitions)))

def one_crawl(graph, v, steps):
    vertices_reached = list()
    for i in range(steps):
        v = graph.get_connected_vertex(v)
        vertices_reached.append(v)
    return vertices_reached


def init_partitions(graph, init_size=10, init_vert=0):
    total_visit_count = [0] * graph.num_vertices
    init_partitions = list()
    for k in range(num_partitions):
        print("Initializing partition ", k)
        partition_visit_count = [0] * graph.num_vertices
        init_verts = list()
        init_verts.append(init_vert)
        init_partitions.append(init_verts)
        for j in range(init_size):
            for i in range(1000):
                verts = one_crawl(graph, init_vert, 20)
                for v in verts:
                    partition_visit_count[v] += 1

            # What a hack!
            flat_list = [item for sublist in init_partitions for item in sublist]
            m = max(t for t in partition_visit_count if partition_visit_count.index(t) not in flat_list)
            init_vert = partition_visit_count.index(m)
            init_verts.append(init_vert)
            init_partitions.pop()
            init_partitions.append(init_verts)
        total_visit_count = [sum(x) for x in zip(partition_visit_count, total_visit_count)]
        init_vert = total_visit_count.index(min(total_visit_count))
    return init_partitions

def assign_partition(graph, partitioning, normalization, assign_v):
    visit_count = np.zeros(graph.num_vertices)
    crawls = 500 - int((sum(normalization)/graph.num_vertices)*400)
    steps = 8 - int((sum(normalization)/graph.num_vertices)*3)
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

partitioning = np.ones(graph.num_vertices, dtype=int) * -1

init_partition_size = 50
init_partitions = init_partitions(graph, init_partition_size)

for k in range(num_partitions):
    partitioning[init_partitions[k]] = k

normalization = np.ones(num_partitions) * init_partition_size

for i in range(graph.num_vertices):
    if partitioning[i] == -1:
        partitioning[i] = assign_partition(graph, partitioning, normalization, i)
        normalization[partitioning[i]] += 1

end = datetime.datetime.now()

print("Partitioned in ", (end - start).total_seconds(), "seconds")

print(normalization)
print(score_partitioning(graph, partitioning))





# # This one will crawl from the partition roots and add vertices and then crawl from the partitions and add vertices. Can easily be scaled to add 10 or 100 vertices at a time.
# def assign_ten_vertices(graph, partitioning):
#     return




# start = datetime.datetime.now()
#
# init_verts = init_vertices(graph, random.randint(0,graph.num_vertices))
#
# partitioning = np.ones(graph.num_vertices, dtype=int) * -1
#
# for i in range(len(init_verts)):
#     partitioning[init_verts[i]] = i
#
# normalization = np.ones(num_partitions)
# for i in range(graph.num_vertices):
#     if partitioning[i] == -1:
#         partitioning[i] = assign_partition(graph, partitioning, normalization, i)
#         normalization[partitioning[i]] += 1
#
# end = datetime.datetime.now()
#
# print("Partitioned in ", (end - start).total_seconds(), "seconds")
#
# print(normalization)
# print(score_partitioning(graph, partitioning))