from utils import *
import numpy as np
from sklearn.cluster import KMeans

#
# def reassign_partitions(graph, partitioning, k, min_score):
#     repartitioning = partitioning.copy()
#     for loops in range(3):
#         reassigned = 0
#         for v1 in range(graph.num_vertices):
#             votes = [0] * k
#             for v2 in graph.edge_dict[v1]:
#                 votes[partitioning[v2]] += 1
#             if votes.index(max(votes)) != repartitioning[v1]:
#                 reassigned += 1
#             repartitioning[v1] = votes.index(max(votes))
#         score = score_partitioning(graph,repartitioning)
#         if score < min_score:
#             min_score = score
#             partitioning = repartitioning.copy()
#         print("Reassigned: ", reassigned)
#         print(score)
#     return partitioning

filename = "Oregon-1.txt"
graph, num_partitions = read_file(filename)
laplacian = graph.laplacian


min_score = 1

while min_score > 0.61:
    vals, vecs = np.linalg.eigh(graph.laplacian)
    vecs = vecs[:, np.argsort(vals)]
    vals = vals[np.argsort(vals)]
    # kmeans on first three vectors with nonzero eigenvalues
    kmeans = KMeans(n_clusters=num_partitions)
    kmeans.fit(vecs[:, 1:20])
    labels = kmeans.labels_
    for i in range(num_partitions):
        print("Num", i, " - ", len([x for x in labels if x == i]))

    score = score_partitioning(graph, labels)
    print("Score:", score)

    if score < min_score:
        min_score = score
        final_partitioning = labels.copy()
    #
    # partitioning = reassign_partitions(graph, labels, num_partitions, score)
    # print("Score after reassignment: ", score_partitioning(graph, partitioning))

write_file(filename, graph, final_partitioning, num_partitions)
