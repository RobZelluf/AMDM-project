from utils import read_file, write_file, Graph, score_partitioning, random_partition, partition_count
import numpy as np
import datetime
from crawl_utils import *
import pickle
import os

# Input prompt for filename
DIRs = [x for x in os.listdir("data/")]
i = 0
for DIR in DIRs:
    print(i, DIR)
    i += 1

data = int(input("Model number:"))
init_partition_size = int(input("Initial partition size:"))

filename = DIRs[data]
graph, num_partitions = read_file(filename)
print("Number of partitions:", num_partitions)
##########


print("Random Partition Score: ", score_partitioning(graph, random_partition(graph, num_partitions)))

start = datetime.datetime.now()

partitioning = np.ones(graph.num_vertices, dtype=int) * -1

threshold = 1 / num_partitions

seed = 0

# blacklist = list()
# partition = list()
# for k in range(num_partitions):
#     partition, seed = grow_monster_partition(graph, seed, init_partition_size, blacklist)
#     partitioning[partition] = k
#     blacklist.append(partition)

init_partitions = init_partitions(graph, num_partitions, init_partition_size, seed)

for k in range(num_partitions):
    partitioning[init_partitions[k]] = k

normalization = partition_count(partitioning)

for i in range(graph.num_vertices):
    if i % 5000 == 0:
        pickle.dump(partitioning, open("save.p", "wb"))
    if partitioning[i] == -1:
        partitioning[i] = assign_partition(graph, partitioning, normalization, i, num_partitions, threshold)
        if partitioning[i] != -1:
            normalization[partitioning[i]] += 1

for i in range(graph.num_vertices):  # Classify edge cases
    if partitioning[i] == -1:
        partitioning[i] = assign_partition(graph, partitioning, normalization, i, num_partitions, 0)
        if partitioning[i] != -1:
            normalization[partitioning[i]] += 1

end = datetime.datetime.now()

print("Partitioned in ", (end - start).total_seconds(), "seconds")

# Reassign bad vertices

print("Counts before reassignment: ", normalization)
print("Score before reassignment: ", score_partitioning(graph, partitioning))

done = 0
for i in range(3):
    majority = 0
    nonmajority = 0
    for v1 in range(graph.num_vertices):
        match = 0
        nonmatch = 0
        for v2 in graph.edge_dict[v1]:
            if partitioning[v1] == partitioning[v2]:
                match += 1
            else:
                nonmatch += 1
        if match > nonmatch:
            majority += 1
        else:
            nonmajority += 1
            partitioning[v1] = abs(partitioning[v1]-1)
    print(majority)
    print(nonmajority)
    print("Counts after reassignment: ", partition_count(partitioning))
    print("Score after reassignment: ", score_partitioning(graph, partitioning))

write_file(filename, graph, partitioning, num_partitions)



#
# partitioning = np.ones(graph.num_vertices, dtype=int) * -1
#
# init_partition_size = 20
# init_partitions = init_partitions(graph, init_partition_size)
#
# for k in range(num_partitions):
#     partitioning[init_partitions[k]] = k
#
# normalization = np.ones(num_partitions) * init_partition_size
#
# for i in range(graph.num_vertices):
#     if partitioning[i] == -1:
#         partitioning[i] = assign_partition(graph, partitioning, normalization, i)
#         normalization[partitioning[i]] += 1






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